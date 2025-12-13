import pytest
from model_bakery import baker
from django.core.exceptions import ValidationError
from store.validators import validate_file_size
from django.core.files.uploadedfile import SimpleUploadedFile


class TestValidateFileSize:

    def test_validate_file_size_with_valid_file(self):
        # Create a file smaller than 1100 KB
        small_file = SimpleUploadedFile(
            "small_file.jpg",
            b"x" * (500 * 1024),  # 500 KB
            content_type="image/jpeg"
        )

        # Should not raise an exception
        try:
            validate_file_size(small_file)
            assert True
        except ValidationError:
            assert False, "Valid file should not raise ValidationError"

    def test_validate_file_size_with_oversized_file(self):
        # Create a file larger than 1100 KB
        large_file = SimpleUploadedFile(
            "large_file.jpg",
            b"x" * (1200 * 1024),  # 1200 KB
            content_type="image/jpeg"
        )

        # Should raise a ValidationError
        with pytest.raises(ValidationError) as exc_info:
            validate_file_size(large_file)

        assert 'File size should not exceed' in str(exc_info.value)

    def test_validate_file_size_exactly_at_limit(self):
        # Create a file exactly 1100 KB
        exact_file = SimpleUploadedFile(
            "exact_file.jpg",
            b"x" * (1100 * 1024),  # 1100 KB
            content_type="image/jpeg"
        )

        # Should not raise an exception
        try:
            validate_file_size(exact_file)
            assert True
        except ValidationError:
            assert False, "File at exact limit should not raise ValidationError"

    def test_validate_file_size_just_over_limit(self):
        # Create a file just over 1100 KB
        over_limit_file = SimpleUploadedFile(
            "over_limit_file.jpg",
            b"x" * (1100 * 1024 + 1),  # 1100 KB + 1 byte
            content_type="image/jpeg"
        )

        # Should raise a ValidationError
        with pytest.raises(ValidationError):
            validate_file_size(over_limit_file)

    def test_validate_file_size_empty_file(self):
        # Create an empty file
        empty_file = SimpleUploadedFile(
            "empty_file.jpg",
            b"",
            content_type="image/jpeg"
        )

        # Should not raise an exception
        try:
            validate_file_size(empty_file)
            assert True
        except ValidationError:
            assert False, "Empty file should not raise ValidationError"
