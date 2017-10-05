# yarasearch

This will scan a directory for files that match a yara rule.

## Example usage:

```
$ ./yarasearch.py -p /mnt -r rules/social_security_numbers.yara
[+] yarasearch.py -- by Daniel Roberson

[+] Scanning files in /mnt
  [+] Desktop/ssns.txt -- Matching rule: SocialSecurityNumbers
  [+] Desktop/Payroll.pdf -- Matching rule: SocialSecurityNumbers

[+] 9 files scanned, 2 hits.
```