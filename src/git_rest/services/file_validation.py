import base64

from git_rest.models.file import FileType


class FileValidation:
    @staticmethod
    def validate_file_type(file_type: str) -> bool:
        return file_type in (FileType.TEXT, FileType.BINARY)

    @staticmethod
    def validate_encoding(content: str, file_type: str) -> bool:
        if file_type == FileType.TEXT:
            try:
                content.encode("utf-8")
                return True
            except Exception:
                return False
        elif file_type == FileType.BINARY:
            try:
                base64.b64decode(content)
                return True
            except Exception:
                return False
        return False

    @staticmethod
    def validate_branch(branch: str, valid_branches: list) -> bool:
        return branch in valid_branches
