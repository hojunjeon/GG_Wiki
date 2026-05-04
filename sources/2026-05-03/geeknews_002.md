---
source: geeknews
date: 2026-05-03
points: 19
url: "https://lasans.blog/articles/misc/email-addresses-deep-dive/"
title: 이메일 주소 심층 분석
---

# 이메일 주소 심층 분석

This article is mainly for people who want to learn more about emails, including founders, developers, marketers, anyone who manages emails, etc. The article is a bit technical and somewhat lengthy.
Basic Structure
Take this email address:
hello@example.com
Three parts:
hello
- the local part, the unique identifier within the domain@
- the separator between the local part and the domainexample.com
- the domain, made up ofexample
and the TLDcom
You have seen this format every day. But behind this familiar structure there are rules, edge cases, and behaviors that most people do not know about. Some matter for security. Some matter for privacy. Some matter when you are building something that needs to handle or validate email addresses. This article covers all of it:
- The local part and all its structures
- The domain part and all its structures
- The top level domain and its many types
- How addresses are fully formatted in different contexts
- The two senders in every email
- Role-based addresses
- Catch-all addresses
- Provider-specific behaviors
- Disposable and temporary email
- Validation and common mistakes
- Security implications
The Local Part
The local part is everything before the @
. Most people think of it as just a username, but there are several valid structures and a few things that are technically allowed but almost never seen in the real world.
Allowed Characters
In the standard unquoted form (called dot-atom in the RFC), the local part allows:
- Letters
a-z
andA-Z
- Digits
0-9
- Special characters:
. _ - + ! # $ % & ' * / = ? ^ { | } ~
The maximum length is 64 octets
. Note that it is octets, not characters. For standard ASCII this makes no practical difference, but for Unicode local parts it matters.
An octet is a computing term for a group of exactly 8 bits, often used interchangeably with
byte
to ensure precision, as a byte historically could vary in size. It is commonly used in networking (IPv4) to represent a0–255
range and is essential for data encoding (e.g.,UTF-8
,Base64
). A64-octet
structure refers to a data block512
bits long.
Case Sensitivity
RFC 5321 technically says the local part is case-sensitive. User@example.com
and user@example.com
could be two separate mailboxes on a strictly compliant server. In practice, every major email provider treats local parts as case-insensitive. Normalizing to lowercase before storing or comparing is the safe default.
The domain part is always case-insensitive. user@EXAMPLE.COM
and user@example.com
are the same address.
Dot Addressing
Dots are allowed in the local part but with three restrictions:
- Cannot start with a dot:
.user@example.com
is invalid - Cannot end with a dot:
user.@example.com
is invalid - Cannot have consecutive dots:
user..name@example.com
is invalid
A valid dot-separated local part:
john.doe@example.com
first.last.name@example.com
a.b.c.d@example.com
Gmail's dot normalization - Gmail ignores dots entirely in the local part. These three addresses all deliver to the exact same inbox:
johndoe@gmail.com
john.doe@gmail.com
j.o.h.n.d.o.e@gmail.com
This is not an RFC
standard. It is Gmail-specific behavior. The consequence is that you can receive email at any dot variation of your Gmail address. More importantly, some services have been tricked by this. A user signs up with johndoe@gmail.com
. An attacker signs up with john.doe@gmail.com
. Many services treat those as two different accounts even though both deliver to the same Gmail inbox. This is a real attack vector for bypassing single-account-per-email restrictions and getting duplicate free trials.
Subaddressing (Plus Addressing)
You can add a tag to the local part using a delimiter, and the mail server delivers the email to the base address while keeping the tag intact in the received message. This is standardized in RFC 5233
.
The most common delimiter is +
:
user+tag@example.com
user+newsletter@gmail.com
user+github@proton.me
The mail server sees user+newsletter@gmail.com
and delivers to user@gmail.com
. The +newsletter
part survives in the email you receive.
Some mail server software uses different delimiters:
+
- the default in Gmail, Outlook, ProtonMail, Fastmail, and most modern systems-
- used in some Yahoo configurations and certain Postfix setups:user-tag@example.com
=
- the default in qmail:user=tag@example.com
The =
delimiter from qmail also explains why VERP (covered below) uses =
to encode the @
sign in the recipient address when building bounce-tracking addresses.
Use cases:
- Tracking leaks - Sign up to each service with a unique tag like
yourname+servicename@gmail.com
. If you start getting spam at that address, you know which service leaked or sold it. - Inbox filtering - Create mail rules that automatically move anything sent to
yourname+newsletters@
into a specific folder. - Multiple accounts - Services that do not normalize the plus away treat
user+tag@domain.com
as different fromuser@domain.com
, letting you create separate accounts on one email address.
One common frustration: many websites have broken email validators that reject +
in a local part even though it is a perfectly valid RFC character. This is a bug in their validation code, not a limitation of email itself.
Quoted String Form
The local part can be wrapped in double quotes, which relaxes most of the character restrictions:
"john doe"@example.com
"user@name"@example.com
"us..er"@example.com
" "@example.com
Inside quotes you can have spaces, @
, (
, )
, ,
, ;
, :
, <
, >
, [
, ]
, and backslash (escaped as \\
). Consecutive dots are valid inside quotes, and leading or trailing dots are also valid inside quotes.
In practice, almost no email provider accepts quoted local parts. Valid per RFC, useless in the real world. You will mainly encounter this when parsing raw email data from old systems or reading the RFC itself.
Comments
Comments in parentheses can appear at the start or end of the local part:
(comment)user@example.com
user(comment)@example.com
Mail servers strip these and they have zero effect on delivery. Technically valid per RFC 5322 but never seen in modern usage.
The reason to know about this: a validator that rejects parentheses in an email address is being stricter than the RFC requires.
Unicode Local Parts (EAI)
RFC 6530
, 6531
, and 6532
define Email Address Internationalization (EAI), which allows UTF-8 characters in the local part. The SMTP session must use the SMTPUTF8
extension for this to work, and both sending and receiving servers must support it.
Adoption is still limited as of 2026. Many servers and services do not support EAI end-to-end. If you are building a system that accepts email addresses, it is worth knowing that technically valid international email addresses exist, even if you choose not to support them yet.
The 64 octet
limit matters more here. A Unicode character can use 2 to 4 octets, so a Unicode-heavy local part can be shorter in visible characters than 64 but still hit the octet limit.
Historical Formats
These are no longer in use but worth knowing because they explain certain characters that are still in the RFC allowed list.
Bang path (UUCP) - Before DNS, email was routed through networks of Unix machines connected by modem (UUCP networks) using a path of hostnames separated by exclamation marks:
machine1!machine2!user
ihnp4!ucbvax!someuser
Read left to right, this tells each machine where to forward the message next. This is where the !
character in the allowed list comes from. Completely dead today.
- Percent hack - A routing trick where
user%otherdomain@relay.com
told the relay server to forward the message touser@otherdomain
. The%
character is still valid in local parts even though this routing mechanism was deprecated inRFC 5321
. Validators that reject%
in a local part are technically wrong. - Source routing - An explicit relay hop list in the SMTP RCPT TO command:
@relay1,@relay2:user@domain
. Also deprecated inRFC 5321
and dead in practice.
VERP (Variable Envelope Return Path)
VERP is a technique used by bulk mail systems to track exactly which recipient caused a bounce. The recipient address is encoded into the envelope sender (the MAIL FROM address), with the @
in the recipient address replaced by =
:
bounces+alice=gmail.com@newsletter.com
When that message bounces, the bounce goes to bounces+alice=gmail.com@newsletter.com
. The sending system knows exactly which recipient caused the failure without any guesswork. Services like Mailchimp, SendGrid, and Amazon SES all use VERP or a variant for bounce processing at scale.
SRS (Sender Rewriting Scheme)
SRS addresses appear when a server forwards mail and rewrites the envelope sender to make SPF checks pass at the final destination. If you look at the raw headers of a forwarded email, you might see something like:
SRS0=HASH=TT=originaldomain.com=originaluser@forwardingdomain.com
Or for multi-hop forwarding:
SRS1=HASH=encodedSRS0@forwardingdomain.com
These are structurally valid email addresses but they are infrastructure artifacts, not human-used addresses. The HASH component is an HMAC over the timestamp and original address, which prevents forgery and limits the token's validity window.
The Domain Part
The domain part is everything between the @
and the end of the address. It is what the sending server uses to look up where to deliver your message.
Label Rules
The domain is made of labels separated by dots. Rules for each label:
- Can contain letters
a-z
, digits0-9
, and hyphens-
- Cannot start or end with a hyphen
- Cannot exceed 63 characters
- Cannot have two consecutive hyphens in positions 3 and 4, unless it is a Punycode label starting with
xn--
The total domain cannot exceed 253 characters. The full email address (local part + @
+ domain) cannot exceed 254 characters.
Subdomains
The domain can have multiple levels:
user@mail.example.com <- one subdomain
user@smtp.mail.example.com <- two subdomains
user@east.prod.mail.example.com <- deeper nesting
Common uses in email:
- Mail infrastructure -
mail.
,smtp.
,mx.
prefixes point to the actual mail server host - Organizational separation -
user@sales.company.com
routes to a different inbox or team thanuser@support.company.com
- ESP sending - Email service providers often send on behalf of a brand from a subdomain like
email.company.com
orsend.company.com
There is no hard limit on subdomain depth beyond the 253-character total domain length.
IP Address Literals
Instead of a domain name, the domain part can be an IP address in square brackets:
user@[192.168.1.1]
user@[IPv6:2001:db8::1]
For IPv6, the IPv6:
tag is required inside the brackets. These are valid per RFC 5321
but are almost never accepted by public mail servers. They are used in internal mail systems and SMTP testing. RFC 5321
also requires that postmaster@[IP.literal]
be accepted by any server that receives mail on that IP.
Single-Label Domains
A domain with no dots is technically valid in some contexts:
user@localhost
user@mailserver
These only work in private or local network environments. Public mail servers reject them. The postmaster@localhost
form is a conventional special case for local system mail on Unix-like systems.
Internationalized Domain Names (IDN) and Punycode
DNS is ASCII-only. To use non-ASCII characters in a domain, they are encoded using Punycode (RFC 3492). Every Punycode-encoded label starts with the prefix xn--
:
xn--mnchen-3ya.de
xn--fsqu00a.xn--0zwm56d
The first example is a German city name with an umlaut encoded in Punycode. The second is a fully internationalized domain where both the name and TLD are encoded. When you see an email address with native-script characters in the domain, what is actually transmitted in SMTP is the xn--
Punycode version. The conversion is transparent in most email clients.
Homograph attacks - Punycode enables visually identical but technically different domains. Characters from different Unicode scripts can look exactly the same but have different code points. An attacker can register a domain that looks like a well-known domain but resolves differently. Browsers have built-in defenses that show Punycode for suspicious IDNs. Email clients mostly do not have these defenses, which makes this attack more effective in email than in web browsing.
The Trailing Dot
In DNS, every domain technically ends with a trailing dot representing the root zone. example.com
is technically example.com.
as a fully qualified domain name. In email, the trailing dot is always implicit and omitted. You will not encounter user@example.com.
in normal use, and most validators reject it even though it is DNS-technically valid.
MX Records
The domain in an email address is not necessarily where the mail server lives. When delivering to user@example.com
, the sending server looks up the MX (Mail Exchanger) DNS records for example.com
. Those records point to the actual mail server hostnames:
example.com MX 10 mail1.provider.com
example.com MX 20 mail2.provider.com
Lower priority number means higher priority. The second entry is a fallback if the first is unavailable. If a domain has no MX records at all, the sending server falls back to the domain's A record.
If a domain should never receive email, it can publish a null MX record:
example.com MX 0 .
The target is just a dot. This explicitly tells sending servers not to attempt delivery. Defined in RFC 7505, this is useful for infrastructure or API-only domains that send mail but should never receive it. It prevents the A-record fallback from being exploited.
The Top Level Domain Part
The TLD is the rightmost label in the domain name. The TLD landscape has changed significantly over time and there are several distinct categories worth knowing.
Original Generic TLDs
The original 7 generic TLDs (gTLDs) from the early internet:
.com
- commercial (now unrestricted, operated by Verisign).net
- network (now unrestricted).org
- organization (now unrestricted).edu
- US accredited educational institutions only (restricted, managed by Educause).gov
- US government entities only (restricted, managed by CISA).mil
- US military only (restricted, managed by the Department of Defense).int
- international organizations established by treaty (very restricted, few domains exist)
There is also .arpa
, an infrastructure TLD managed by IANA. Not for public registration. You see it in reverse DNS lookups like 1.0.0.127.in-addr.arpa
.
Country Code TLDs (ccTLDs)
Two-letter codes based on ISO 3166-1 alpha-2 country codes. Around 250 of them exist. Each country's registry sets its own registration rules, residency requirements, and pricing.
Some ccTLDs have been repurposed by other industries entirely:
.io
(British Indian Ocean Territory) - widely used by tech companies and startups.tv
(Tuvalu) - used by media and streaming services.ai
(Anguilla) - used by AI companies.co
(Colombia) - used as a company-focused alternative to.com
.me
(Montenegro) - used for personal sites and services.ly
(Libya) - used by URL shorteners.sh
(Saint Helena) - used by software projects and developer tools
When you use a repurposed ccTLD, you are technically under the registry of that country with all the legal and political implications that come with it. The original country's registry controls the domain, not ICANN.
Sponsored TLDs (sTLDs)
Sponsored TLDs have a sponsoring organization and eligibility requirements:
.aero
- air transport industry (sponsored by SITA).coop
- cooperative organizations.museum
- museums (operated by MuseDoma).jobs
- employment sector.xxx
- adult entertainment.post
- postal services (Universal Postal Union).cat
- Catalan language and culture
Note that .edu
, .gov
, and .mil
from the original gTLD set are also technically sponsored TLDs since they have specific eligibility requirements.
New Generic TLDs (Post-2012)
In 2012, ICANN opened applications for new generic TLDs. Over 1,200 new TLDs have been delegated since then.
This matters for email validation for one specific reason: any validator that limits TLD length to 4 to 6 characters is broken. TLDs like .photography
, .international
, .construction
, and .technologies
are valid and in use.
Some common new gTLDs:
- Developer-focused:
.app
,.dev
,.web
,.code
- Commerce:
.shop
,.store
,.online
,.market
- Content:
.blog
,.news
,.media
,.video
- Business:
.tech
,.agency
,.solutions
,.services
,.cloud
New gTLDs are disproportionately represented in spam and phishing due to low registration costs and weaker abuse policies at some registries.
Brand TLDs
Large companies applied for their own TLDs during the 2012 ICANN expansion:
.google
,.youtube
,.gmail
.apple
,.microsoft
,.amazon
.chase
,.barclays
,.bmw
Most brand TLDs are not used for public email addresses. .gmail
exists as a TLD but Google does not issue user@something.gmail
addresses. They are mainly used for internal purposes or not at all.
Geographic and City TLDs
Cities and regions have their own TLDs:
.nyc
,.london
,.paris
,.berlin
,.tokyo
,.sydney
.wales
,.scot
,.bzh
(Brittany)
Registration usually requires a demonstrated connection to the geographic area.
Internationalized TLDs
TLDs in non-ASCII scripts exist for many countries. These are Punycode-encoded in DNS:
.xn--p1ai
- Russia (Cyrillic script).xn--fiqz9s
- China (simplified Chinese script).xn--fiqs8sirgfmh
- China (also simplified Chinese, different encoding).xn--mgberp4a5d4ar
- Saudi Arabia (Arabic script).xn--h2brj9c
- India (Devanagari script)
Email clients display these in their native script while SMTP transmits the Punycode form (unless the SMTPUTF8 extension is active).
Reserved and Documentation TLDs
RFC 2606 and RFC 6761 reserve certain TLDs for testing and documentation:
.test
- guaranteed never to be in public DNS, safe for software testing.example
- for documentation examples.invalid
- for contexts where a provably non-resolving domain is needed.localhost
- for loopback use
At the second level, IANA registered example.com
, example.net
, and example.org
specifically for use in documentation and examples. These domains exist but have no MX records. Use them freely in code examples and documentation without worrying about hitting a real mailbox.
Retired TLDs
Some ccTLDs were removed when the country they represented ceased to exist:
.yu
- Yugoslavia (deleted 2010).cs
- Czechoslovakia (deleted 1995).dd
- East Germany (deleted 1990 after reunification).tp
- East Timor (replaced by.tl
, fully deleted 2015)
One notable exception: .su
(Soviet Union) still has active domains despite the USSR dissolving in 1991. IANA has been in ongoing transition discussions for years but it remains active.
Second-Level Domains in ccTLDs
Many country code TLDs add a functional second-level category between the registrable name and the TLD, similar to how gTLDs work. The effective TLD for registration purposes is two labels, not one.
Some examples by country:
- United Kingdom -
.co.uk
(commercial),.org.uk
,.gov.uk
,.me.uk
,.sch.uk
(schools),.nhs.uk
- Australia -
.com.au
,.net.au
,.org.au
,.edu.au
,.gov.au
,.id.au
(individuals) - Japan -
.co.jp
,.ne.jp
,.or.jp
,.ac.jp
,.go.jp
- India -
.co.in
,.net.in
,.org.in
,.gov.in
,.edu.in
- Brazil -
.com.br
,.net.br
,.org.br
,.gov.br
So for user@example.co.uk
:
user
is the local partexample
is the registrable domain.co.uk
is the effective TLD
This affects email validation and organizational domain detection, which matters for email authentication systems that need to find the root domain for a given address.
The Public Suffix List
The Public Suffix List (PSL) at publicsuffix.org
is a community-maintained list of all domain suffixes under which internet users can directly register names. It covers both official delegations like .co.uk
and .com.au
, and private registries like github.io
, wordpress.com
, and herokuapp.com
.
The PSL uses wildcard notation. For example, *.ck
means every second-level under .ck
is treated as a public suffix. Exceptions are noted with !
: !www.ck
means www.ck
specifically is not a public suffix.
Email validators and spam filters use the PSL to identify the organizational domain from a full domain string. It is not an IETF standard but it is the de facto standard for this problem.
How Email Addresses Are Formatted
The raw local@domain
string is called an addr-spec. But there are several ways a complete email address can appear depending on the context it is used in.
Bare Address
Just the addr-spec, used in SMTP commands and simple contexts:
user@example.com
Angle Bracket Format
In SMTP, the address is wrapped in angle brackets in the MAIL FROM and RCPT TO commands:
MAIL FROM:<sender@example.com>
RCPT TO:<recipient@example.com>
The angle brackets are part of the SMTP command syntax, not the address itself.
Display Name Format
In message headers (From, To, Cc), a human-readable name can precede the angle-bracketed address:
"John Doe" <john@example.com>
John Doe <john@example.com>
Quotes around the display name are required if it contains special characters. They are optional if it is just plain words.
Display name spoofing - The display name can be set to absolutely anything by the sender. An attacker can write:
"PayPal Security <paypal@paypal.com>" <attacker@evil.com>
In many email clients, only the display name is shown in the inbox list view. The display name above looks exactly like a real PayPal address. The actual sending address is only visible when you expand the From field. This is one of the most common phishing techniques and it works because it exploits the way email clients display the sender.
Group Syntax
RFC 5322 defines a named group format for multiple recipients:
Marketing Team: alice@example.com, "Bob Smith" <bob@example.com>;
Group name, colon, comma-separated addresses, semicolon at the end. A common use of this is the undisclosed recipients pattern:
To: undisclosed-recipients:;
Empty group syntax. The actual recipients are in the SMTP envelope (RCPT TO commands) and are not visible in the message headers. Standard practice for bulk mail and BCC-only sends.
Encoded Display Names
In older email systems, non-ASCII characters in display names are encoded using RFC 2047 encoded words:
=?UTF-8?B?SGVsbG8gV29ybGQ=?=
The format is =?charset?encoding?encoded_text?=
where encoding is B
(base64) or Q
(quoted-printable). You encounter this when parsing raw email headers from older systems. With modern SMTPUTF8 support, UTF-8 can be used directly in headers without this encoding wrapper.
The Two Senders in Every Email
Every email has two separate sender addresses. Most people do not know this and it is the root cause of most email spoofing confusion.
The Envelope Sender (MAIL FROM)
Set in the SMTP MAIL FROM:
command during transmission. This address:
- Is not part of the message content itself
- Is used for bounce routing - any delivery failure reports go here
- Is what SPF checks when validating the sender
- Is stored as the
Return-Path:
header by the final receiving server - Is also called the envelope from, reverse path, or RFC5321.MailFrom
The From Header
The address in the From:
header of the message. This is what your email client shows you as the sender. This address:
- Is what DMARC protects in combination with SPF or DKIM alignment
- Is freely settable by the sender with no inherent validation by most mail servers
- Is what display name spoofing and domain impersonation targets
These two addresses can be completely different. This is normal and expected in many legitimate scenarios:
- ESP bulk sending - MAIL FROM is
bounce@esp.com
for bounce handling, while the From header showsnewsletter@yourbrand.com
- Mailing lists - MAIL FROM is the list's bounce address, From header shows the original poster
- Email forwarding - the forwarding server rewrites MAIL FROM using SRS to pass SPF checks at the final destination, while the From header stays as the original sender
Without DMARC enforcement on a domain, anyone can send email with that domain in the From header while using a completely unrelated MAIL FROM. This is how domain impersonation in phishing works.
The Sender Header
When the actual submitter of a message differs from the From address, the Sender:
header identifies who actually sent it:
From: Brand Newsletter <newsletter@company.com>
Sender: mailer@sendgrid.net
The Reply-To Header
Specifies where replies should go, which can differ from the From address:
From: newsletter@company.com
Reply-To: support@company.com
This is also a phishing vector. An attacker sets From to a legitimate-looking address and Reply-To to their own address. The victim thinks they are replying to the real sender.
The Null Sender
MAIL FROM:<>
is a valid and important SMTP construct. An empty envelope sender is used for bounce messages, autoresponders, and any message that must not itself generate a bounce. This prevents infinite bounce loops from occurring when two systems keep exchanging failure notifications.
Role-Based Addresses
Some email addresses represent functional roles rather than individual people. RFC 2142 defines which ones should exist at every domain.
Required by RFC 5321
One address is mandatory for every domain that accepts mail:
postmaster@domain
- RFC 5321 requires every mail-accepting domain to accept mail at this address, no exceptions. If you run a mail server, this must work. The RFC also requires thatpostmaster@[IP.address]
in IP literal format be accepted by any server that receives mail on that IP.
Recommended by RFC 2142
Beyond postmaster, RFC 2142 recommends these role addresses:
abuse@domain
- for reporting spam and abuse, used by ISPs and anti-spam organizationshostmaster@domain
- DNS zone administrationsecurity@domain
- vulnerability disclosures and security reportswebmaster@domain
- web server issuesnoc@domain
- network operations, relevant for network providers and ISPs
Conventional Role Addresses
No formal standard, but widely used conventions you will see everywhere:
info@
, support@
, sales@
, billing@
, legal@
, privacy@
, careers@
, contact@
, hello@
, help@
, feedback@
, admin@
Most organizations implement some subset of these. None of them are RFC-required.
One thing worth noting: role addresses are typically shared among multiple people. Sending sensitive information to support@company.com
means multiple team members can read it. And abuse@
and postmaster@
receive complaint mail which makes them targets for social engineering.
Catch-All Addresses
A catch-all is not a specific email address format. It is a mail server configuration that accepts delivery for any local part at a domain, even if no specific mailbox exists for that address:
anythingatall@yourdomain.com <- delivered
doesnotexist@yourdomain.com <- also delivered
Use cases:
- Catching typos - a business wants
saels@company.com
to still reach the sales team - Developer testing - any test address works without pre-creating individual inboxes
- Privacy - generate unique addresses per service without a formal alias system
The downside is significant. Catch-all domains attract large volumes of spam because any local part delivers. It also makes address validation impossible via SMTP probing, since every probe returns a successful response regardless of whether a real inbox exists.
Provider-Specific Behaviors
Beyond the RFC standards, individual email providers have their own quirks that affect how addresses behave.
Gmail
- Dot normalization - Gmail ignores all dots in the local part.
johndoe@gmail.com
andj.o.h.n.d.o.e@gmail.com
are the same inbox. - Plus addressing - Supported with
+
as the delimiter. @googlemail.com
- A historical alias for@gmail.com
due to trademark disputes in Germany and the UK. Both domains deliver to the same inbox.- Character restrictions - Gmail only allows letters, digits, and dots in local parts (plus
+
for subaddressing). The full RFC character set is not supported. - Local part length limit - 30 characters, well below the RFC maximum of 64.
Microsoft (Outlook, Hotmail, Live)
- No dot normalization -
johndoe@outlook.com
andjohn.doe@outlook.com
are different mailboxes. - Domain aliases -
@hotmail.com
,@live.com
, and@outlook.com
can all refer to the same account if aliases are configured. - Plus addressing - Supported.
Apple (iCloud)
- Domain aliases -
@icloud.com
,@me.com
, and@mac.com
are the same inbox. This is a result of Apple renaming the service over the years: .mac became .me became .icloud. - Plus addressing - Supported.
- Hide My Email - Generates random aliases in the format
randomstring@privaterelay.appleid.com
that forward to your real address. Each service or app can get a unique alias, keeping your real address private.
ProtonMail / Proton
- Domain aliases -
@proton.me
,@protonmail.com
, and@pm.me
are the same inbox. - Plus addressing - Supported.
Email Aliasing Services
Separate from disposable email, aliasing services create permanent, controllable forwarding addresses:
- SimpleLogin (part of Proton) - custom or random aliases that forward to any inbox
- Addy.io (formerly AnonAddy) - similar to SimpleLogin, can be self-hosted
- Firefox Relay (Mozilla) - random aliases with limits on the free plan
- DuckDuckGo Email Protection -
@duck.com
aliases
These generate addresses that are structurally indistinguishable from real inboxes to the sender. The key difference from disposable email: aliases are permanent and you control them. You can disable specific ones, see which service sent what, and forward to any inbox you own.
Disposable and Temporary Email
Disposable email services provide inboxes that require no signup and typically expire after a short period. Common services include Mailinator, Guerrilla Mail, 10 Minute Mail, and TempMail.
Most use catch-all routing, so any local part at the domain delivers to an inbox. Many of those inboxes are public, meaning anyone who knows the address can read the messages.
Blocklists of known disposable domains exist (the disposable-email-domains
GitHub repository is the most commonly referenced), but they are always incomplete. These services constantly rotate to new domains to evade blocklisting, so any hardcoded list goes stale quickly.
Validation
Technical Validity vs Practical Validity
There is a gap between what the RFC says is valid and what works in the real world.
Technically valid per RFC but almost never accepted by real servers:
" "@example.com <- space in local part (inside quotes)
"user@name"@example.com <- at-sign in local part (inside quotes)
user@[192.168.1.1] <- IP literal domain
a@b <- single-char local, single-label domain
Technically valid and practically accepted:
user+tag@example.com
user_name@example.com
user@subdomain.example.co.uk
user@example.photography
For most applications, a pragmatic validator beats a fully RFC-compliant one. Check the basic structure, verify the character set is reasonable, and optionally do a DNS MX lookup on the domain. Trying to be fully RFC-compliant leads to accepting addresses that real mail systems reject.
Common Validator Bugs
These are specific bugs that appear frequently enough to be worth calling out:
- Rejecting
+
in local parts -user+tag@example.com
is completely valid. Very common bug. - Rejecting
_
in local parts - Also valid. - Rejecting
%
in local parts - Valid character. Only the percent-hack routing use is deprecated, not the character itself. - Limiting TLD length to 4 to 6 characters - Breaks
.photography
,.international
,.construction
, and hundreds of other new gTLDs. - Validating against a hardcoded TLD list - The list changes constantly. Hardcoding it means your validator goes stale.
- Wrong total length limit - Using 255 or 256 instead of 254. RFC 3696 errata number 1690 corrected the widely-cited wrong value of 320 down to 254.
- Rejecting uppercase in local parts - Valid per RFC.
- Rejecting
user@subdomain.co.uk
- Valid. Multi-dot domains with second-level ccTLD patterns are fine. - Rejecting
.dev
,.app
,.io
as TLDs - These are all valid delegated TLDs.
Length Limits
The local part limit is in octets, not characters. For EAI addresses with multibyte Unicode characters, a local part can have fewer visible characters than 64 but still hit the octet limit.
DNS-Based Validation
Beyond syntax, you can check whether an address is likely deliverable:
- MX record check - Verify the domain has MX records. Fast, low-risk, handles most cases. Note that domains using A-record fallback (no MX configured) will fail this check even if they accept mail.
- Null MX check - If the domain has
MX 0 .
, it explicitly does not accept mail. Any address at that domain is definitely undeliverable. - SMTP RCPT TO probing - Connect to the mail server and issue a RCPT TO command to check if the address is accepted. Unreliable because many servers respond with 250 to any address to prevent harvesting. Catch-all domains always respond positively. This approach also risks getting your probe IP blacklisted.
The only fully reliable way to verify an email address is to send a message to it and check if it arrives. Everything else is a heuristic.
Security Implications
Display Name Spoofing
Anyone can set the display name in an email to anything they want. In inbox views that show only the display name, users cannot tell the difference between a legitimate sender and an impersonated one without explicitly checking the actual address. Email clients that show only the name in list view make this attack trivial to execute. Always expand the From field to see the actual address before trusting a message.
Homograph Attacks via Punycode
Domains that look visually identical to real well-known domains can be registered using characters from different Unicode scripts. Email clients generally do not display any warnings about this the way browsers do. A message appearing to come from a domain that looks like a major brand but uses a lookalike character from a different script is a completely different domain with a different owner.
Gmail Dot Trick for Account Bypass
Because Gmail ignores dots, attackers can sign up to a service using a dot-variant of an existing Gmail address. The service treats it as a new account while all email still delivers to the original inbox. This is used to bypass single-account-per-email restrictions, claim duplicate free trials, and sometimes to receive email intended for the original account holder.
Email Address Reuse
Email providers can reassign abandoned addresses to new users. The new account owner then receives account recovery emails from services the previous owner was registered with, potentially allowing account takeover via password reset. Gmail claims they do not reassign addresses. Some other providers have done so historically.
Subaddress Tag Exposure
When you use user+newsletter@gmail.com
to sign up somewhere, the receiving service sees the full address including the tag. Services that strip the plus tag before storing it expose your base address anyway. Those that store the full address as-is reveal your tracking strategy if they ever display it back to you in account settings or data exports.
Additional
Now you have an idea of what email addresses are, how they can be used to abuse free tiers, and how users can spam your product or email lists. If you collect email addresses anywhere, try Autheona for free.
~ Lasan