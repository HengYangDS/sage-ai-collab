"""Semantic Search Plugin for SAGE Knowledge Base.

This plugin provides semantic search capabilities using TF-IDF
based similarity matching for knowledge content.

Version: 0.1.0
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from sage.plugins.base import PluginMetadata, SearchPlugin

if TYPE_CHECKING:
    pass

__all__ = ["SemanticSearchPlugin", "SearchDocument", "SearchConfig"]


@dataclass
class SearchDocument:
    """A document indexed for search."""

    id: str
    content: str
    title: str = ""
    layer: str = ""
    path: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    # Computed fields for TF-IDF
    terms: Counter[str] = field(default_factory=Counter)
    term_frequencies: dict[str, float] = field(default_factory=dict)


@dataclass
class SearchConfig:
    """Configuration for semantic search."""

    min_term_length: int = 2
    max_results: int = 20
    score_threshold: float = 0.1
    use_stemming: bool = False
    stopwords: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        """Initialize default stopwords."""
        if not self.stopwords:
            self.stopwords = {
                "a", "an", "the", "and", "or", "but", "in", "on", "at",
                "to", "for", "of", "with", "by", "from", "is", "are",
                "was", "were", "be", "been", "being", "have", "has",
                "had", "do", "does", "did", "will", "would", "could",
                "should", "may", "might", "must", "shall", "can",
                "this", "that", "these", "those", "it", "its",
            }


@dataclass
class SearchResult:
    """A search result with relevance score."""

    document: SearchDocument
    score: float
    matched_terms: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.document.id,
            "title": self.document.title,
            "layer": self.document.layer,
            "path": self.document.path,
            "score": round(self.score, 4),
            "matched_terms": self.matched_terms,
            "snippet": self._get_snippet(),
        }

    def _get_snippet(self, max_length: int = 200) -> str:
        """Get a content snippet."""
        content = self.document.content
        if len(content) <= max_length:
            return content
        return content[:max_length].rsplit(" ", 1)[0] + "..."


class SemanticSearchPlugin(SearchPlugin):
    """TF-IDF based semantic search plugin.

    Provides semantic search capabilities:
    - TF-IDF based document indexing
    - Cosine similarity scoring
    - Configurable stopwords and stemming
    - Result ranking and filtering

    Configuration options (via sage.yaml):
        min_term_length: Minimum term length to index (default: 2)
        max_results: Maximum results to return (default: 20)
        score_threshold: Minimum score threshold (default: 0.1)
        use_stemming: Enable basic stemming (default: False)

    Example:
        >>> plugin = SemanticSearchPlugin()
        >>> plugin.index_document("doc1", "Hello world content", layer="core")
        >>> results = plugin.search("world")
    """

    def __init__(self, config: SearchConfig | None = None) -> None:
        """Initialize the semantic search plugin.

        Args:
            config: Optional search configuration.
        """
        self._metadata = PluginMetadata(
            name="semantic_search",
            version="0.1.0",
            description="TF-IDF based semantic search for knowledge content",
            author="SAGE Team",
            hooks=["pre_search", "post_search"],
        )

        self.config = config or SearchConfig()
        self._documents: dict[str, SearchDocument] = {}
        self._document_frequencies: Counter[str] = Counter()
        self._total_documents = 0
        self._enabled = True

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        return self._metadata

    def configure(self, config: dict[str, Any]) -> None:
        """Configure the plugin from settings.

        Args:
            config: Configuration dictionary.
        """
        self.config.min_term_length = config.get(
            "min_term_length", self.config.min_term_length
        )
        self.config.max_results = config.get("max_results", self.config.max_results)
        self.config.score_threshold = config.get(
            "score_threshold", self.config.score_threshold
        )
        self.config.use_stemming = config.get("use_stemming", self.config.use_stemming)
        self._enabled = config.get("enabled", True)

        if "stopwords" in config:
            self.config.stopwords = set(config["stopwords"])

    def on_load(self, context: dict[str, Any]) -> None:
        """Handle plugin load event."""
        self._documents.clear()
        self._document_frequencies.clear()
        self._total_documents = 0

    def on_unload(self) -> None:
        """Handle plugin unload event."""
        self._documents.clear()
        self._document_frequencies.clear()

    def on_enable(self) -> None:
        """Handle plugin enable event."""
        self._enabled = True

    def on_disable(self) -> None:
        """Handle plugin disable event."""
        self._enabled = False

    # SearchPlugin hooks

    def pre_search(
        self,
        query: str,
        options: dict[str, Any],
    ) -> tuple[str, dict[str, Any]]:
        """Preprocess search query.

        Args:
            query: The search query.
            options: Search options.

        Returns:
            Tuple of (processed query, modified options).
        """
        # Normalize query
        processed_query = query.lower().strip()

        # Add semantic search flag
        options["semantic_enabled"] = self._enabled
        options["original_query"] = query

        return processed_query, options

    def post_search(
        self,
        results: list[dict[str, Any]],
        query: str,
    ) -> list[dict[str, Any]]:
        """Post-process search results with semantic ranking.

        Args:
            results: Initial search results.
            query: The search query.

        Returns:
            Ranked search results.
        """
        if not self._enabled or not self._documents:
            return results

        # Perform semantic search
        semantic_results = self.search(query)

        # Merge with existing results
        result_ids = {r.get("id") for r in results}

        for sr in semantic_results:
            if sr.document.id not in result_ids:
                results.append(sr.to_dict())

        # Sort by score
        results.sort(key=lambda x: x.get("score", 0), reverse=True)

        return results[: self.config.max_results]

    # Indexing methods

    def index_document(
        self,
        doc_id: str,
        content: str,
        title: str = "",
        layer: str = "",
        path: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Index a document for search.

        Args:
            doc_id: Unique document identifier.
            content: Document content.
            title: Document title.
            layer: Knowledge layer.
            path: File path.
            metadata: Additional metadata.
        """
        # Create document
        doc = SearchDocument(
            id=doc_id,
            content=content,
            title=title,
            layer=layer,
            path=path,
            metadata=metadata or {},
        )

        # Tokenize and count terms
        terms = self._tokenize(content)
        if title:
            # Title terms weighted higher
            title_terms = self._tokenize(title)
            terms.extend(title_terms * 2)

        doc.terms = Counter(terms)

        # Calculate term frequencies
        total_terms = len(terms)
        if total_terms > 0:
            doc.term_frequencies = {
                term: count / total_terms for term, count in doc.terms.items()
            }

        # Update document frequencies
        if doc_id in self._documents:
            # Remove old document's contribution
            old_doc = self._documents[doc_id]
            for term in old_doc.terms:
                self._document_frequencies[term] -= 1
        else:
            self._total_documents += 1

        # Add new document's contribution
        for term in doc.terms:
            self._document_frequencies[term] += 1

        self._documents[doc_id] = doc

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document from the index.

        Args:
            doc_id: Document identifier.

        Returns:
            True if document was removed, False if not found.
        """
        if doc_id not in self._documents:
            return False

        doc = self._documents.pop(doc_id)
        self._total_documents -= 1

        for term in doc.terms:
            self._document_frequencies[term] -= 1
            if self._document_frequencies[term] <= 0:
                del self._document_frequencies[term]

        return True

    # Search methods

    def search(self, query: str) -> list[SearchResult]:
        """Search for documents matching the query.

        Args:
            query: Search query.

        Returns:
            List of search results sorted by relevance.
        """
        if not self._enabled or not self._documents:
            return []

        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        # Calculate query TF-IDF vector
        query_vector = self._calculate_query_vector(query_terms)

        # Score each document
        results: list[SearchResult] = []
        for doc in self._documents.values():
            score, matched = self._calculate_similarity(query_vector, doc)
            if score >= self.config.score_threshold:
                results.append(
                    SearchResult(document=doc, score=score, matched_terms=matched)
                )

        # Sort by score
        results.sort(key=lambda r: r.score, reverse=True)

        return results[: self.config.max_results]

    # Private methods

    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text into terms.

        Args:
            text: Text to tokenize.

        Returns:
            List of terms.
        """
        # Convert to lowercase and extract words
        text = text.lower()
        words = re.findall(r"\b[a-z0-9]+\b", text)

        # Filter by length and stopwords
        terms = [
            word
            for word in words
            if len(word) >= self.config.min_term_length
            and word not in self.config.stopwords
        ]

        # Apply basic stemming if enabled
        if self.config.use_stemming:
            terms = [self._stem(term) for term in terms]

        return terms

    def _stem(self, word: str) -> str:
        """Apply basic stemming to a word.

        Args:
            word: Word to stem.

        Returns:
            Stemmed word.
        """
        # Very basic suffix stripping
        suffixes = ["ing", "ed", "er", "est", "ly", "tion", "ness"]
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                return word[: -len(suffix)]
        return word

    def _calculate_query_vector(
        self, query_terms: list[str]
    ) -> dict[str, float]:
        """Calculate TF-IDF vector for query.

        Args:
            query_terms: List of query terms.

        Returns:
            Dictionary of term -> TF-IDF weight.
        """
        term_counts = Counter(query_terms)
        total_terms = len(query_terms)
        vector: dict[str, float] = {}

        for term, count in term_counts.items():
            tf = count / total_terms
            idf = self._calculate_idf(term)
            vector[term] = tf * idf

        return vector

    def _calculate_idf(self, term: str) -> float:
        """Calculate IDF for a term.

        Args:
            term: The term.

        Returns:
            IDF value.
        """
        if self._total_documents == 0:
            return 0.0

        doc_freq = self._document_frequencies.get(term, 0)
        if doc_freq == 0:
            return 0.0

        return math.log(self._total_documents / doc_freq) + 1

    def _calculate_similarity(
        self,
        query_vector: dict[str, float],
        doc: SearchDocument,
    ) -> tuple[float, list[str]]:
        """Calculate cosine similarity between query and document.

        Args:
            query_vector: Query TF-IDF vector.
            doc: Document to compare.

        Returns:
            Tuple of (similarity score, matched terms).
        """
        matched_terms: list[str] = []
        dot_product = 0.0
        query_norm = 0.0
        doc_norm = 0.0

        # Calculate dot product and query norm
        for term, query_weight in query_vector.items():
            query_norm += query_weight * query_weight

            if term in doc.term_frequencies:
                matched_terms.append(term)
                doc_tf = doc.term_frequencies[term]
                idf = self._calculate_idf(term)
                doc_weight = doc_tf * idf
                dot_product += query_weight * doc_weight

        # Calculate doc norm for matched terms
        for term in doc.term_frequencies:
            doc_tf = doc.term_frequencies[term]
            idf = self._calculate_idf(term)
            doc_weight = doc_tf * idf
            doc_norm += doc_weight * doc_weight

        # Calculate cosine similarity
        if query_norm == 0 or doc_norm == 0:
            return 0.0, matched_terms

        similarity = dot_product / (math.sqrt(query_norm) * math.sqrt(doc_norm))
        return similarity, matched_terms

    def get_stats(self) -> dict[str, Any]:
        """Get search index statistics.

        Returns:
            Dictionary of statistics.
        """
        return {
            "total_documents": self._total_documents,
            "unique_terms": len(self._document_frequencies),
            "enabled": self._enabled,
            "config": {
                "min_term_length": self.config.min_term_length,
                "max_results": self.config.max_results,
                "score_threshold": self.config.score_threshold,
                "use_stemming": self.config.use_stemming,
            },
        }

    def clear(self) -> None:
        """Clear the search index."""
        self._documents.clear()
        self._document_frequencies.clear()
        self._total_documents = 0
