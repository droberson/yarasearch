# yarascan

This will scan a directory for files that match a yara rule.

## Example usage:

```
$ ./yarascan.py -p /mnt -r rules/social_security_numbers.yara
[+] yarascan.py -- by Daniel Roberson

[+] Scanning files in /mnt
  [+] Desktop/ssns.txt -- Matching rule: SocialSecurityNumbers
  [+] Desktop/Payroll.pdf -- Matching rule: SocialSecurityNumbers

[+] 9 files scanned, 2 hits.
```