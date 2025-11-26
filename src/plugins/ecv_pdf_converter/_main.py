# This is a custom plugin for PDF Converter.

import sys
import io
from typing import BinaryIO, Any

from markitdown import (
    DocumentConverter,
    DocumentConverterResult,
    StreamInfo,
    MissingDependencyException,
)

from error import MISSING_DEPENDENCY_MESSAGE

# Import helpers
from .utils import process_page_legacy, process_page

_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
    import pdfplumber
except ImportError:
    _dependency_exc_info = sys.exc_info()

ACCEPTED_FILE_EXTENSIONS = [".pdf"]

class ECVPDFConverter(DocumentConverter):
    """Custom converter acts as markitdown plugin. Is supports only for
    machine-generated pdf, not scanned one.

    Args:
        DocumentConverter (DocumentConverter): base class of document converter.
    """

    def __init__(self):
        super().__init__()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        # for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
        #     if mimetype.startswith(prefix):
        #         return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[1].with_traceback(_dependency_exc_info[2])

        assert isinstance(file_stream, io.IOBase)

        markdown_chunks: list[str] = []

        try:
            with pdfplumber.open(file_stream) as pdf:
                for page in pdf.pages:
                    markdown_chunk = process_page(page)
                    markdown_chunks.append(markdown_chunk)

            markdown = "\n\n".join(markdown_chunks).strip()

        except Exception as e:
            markdown = pdfminer.high_level.extract_text(file_stream)

        if not markdown:
            markdown = pdfminer.high_level.extract_text(file_stream)

        return DocumentConverterResult(markdown=markdown)
