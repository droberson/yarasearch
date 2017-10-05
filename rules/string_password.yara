rule StringPassword
{
    strings:
        $text_string = "password" nocase

    condition:
        $text_string
}