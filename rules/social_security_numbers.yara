rule SocialSecurityNumbers
{
    strings:
        $re1 = /\d{3}-\d{2}-\d{4}/
        $re2 = /\d{9}/
	$string1 = "Social Security Number"
	$string2 = "SSN"

    condition:
        $re1 or $re2 or $string1 or $string2
}

