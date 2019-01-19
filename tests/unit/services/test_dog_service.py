from services.dog_service import sanitize_string


class TestSanitizeString:

    def test_sanitize_string_with_numbers(self):
        french_with_numbers = "380frenc33h bulldo9g"
        expected = "french bulldog"

        assert expected == sanitize_string(french_with_numbers)
