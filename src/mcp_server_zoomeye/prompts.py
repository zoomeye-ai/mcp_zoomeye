SEARCH_SYNTAX_GUIDE = """
### Search Syntax Guide

- Search Scope covers devices (IPv4, IPv6) and websites (domains).
- When entering a search string, the system will match keywords in "global" mode, including content from various
  protocols such as HTTP, SSH, FTP, etc. (e.g., HTTP/HTTPS protocol headers, body, SSL, title, and other protocol
  banners).
- Search strings are case-insensitive and will be segmented for matching (the search results page provides a "
  segmentation" test feature). When using == for search, it enforces exact case-sensitive matching with strict syntax.
- Please use quotes for search strings (e.g., "Cisco System" or 'Cisco System'). If the search string contains quotes,
  use the escape character, e.g.,"a\"b". If the search string contains parentheses, use the escape character, e.g.,
  portinfo\(\).

### The logical operators of the syntax：

- =， Search for assets containing keywords
  title="knownsec"
  Search for websites with titles containing Knownsec's assets
- ==， Accurate search, indicating a complete match of keywords (case sensitive), can search for data with empty values
  title=="knownsec"
  Precise search, which means exact match of keywords (case sensitive), and can search for data with empty values Search
  for assets with the website title "Knownsec"
- ||， Enter "||" in the search box to indicate the logical operation of "or"
  service="ssh" || service="http"
  Search for SSH or HTTP data
- &&， Enter "&&" in the search box to indicate the logical operation of "and"
  device="router" && after="2020-01-01"
  Search for routers after Jan 1, 2020
- !=， Enter "!=" in the search box to indicate the logical operation of "not"
  country="US" && subdivisions!="new york"
  Search for data in united states excluding new york
- ()， Enter "()" in the search box to indicate the logical operation of "priority processing"
  (country="US" && port!=80) || (country="US" && title!="404 Not Found")
  Search excluding port 80 in US or "404 not found" in the US
- *，Fuzzy search, use * for search
  title="*google"
  Fuzzy search, use * to search Search for assets containing Knowsec in the website title, and the title can start with
  any character

### Grammatical keywords

#### Geographical Location Search

- country="CN"    Search for country assets
  Input country abbreviations or names, e.g.
  country="china"
- subdivisions="beijing"  Search for assets in the specified administrative region
  Input in English, e.g.
  subdivisions="beijing"
- city="changsha" Search for city assets
  Input in English, e.g.
  city="changsha"

#### Certificate Search

- ssl="google"    Search for assets with "google" string in ssl certificate Often used to search for corresponding
  targets by product name and company name
- ssl.cert.fingerprint="F3C98F223D82CC41CF83D94671CCC6C69873FABF" Search for certificate-related fingerprint assets
- ssl.chain_count=3 Search for SSL chain count assets
- ssl.cert.alg="SHA256-RSA"   Search for signature algorithms supported by certificates
- ssl.cert.issuer.cn="pbx.wildix.com" Search for the common domain name of the user certificate issuer
- ssl.cert.pubkey.rsa.bits=2048 Search for rsa_bits certificate public key bit number
- ssl.cert.pubkey.ecdsa.bits=256 Search for ecdsa_bits certificate public key bit number
- ssl.cert.pubkey.type="RSA"  Search for the public key type of the certificate
- ssl.cert.serial="18460192207935675900910674501" Search for certificate serial number
- ssl.cipher.bits="128"   Search for encryption suite bit number
- ssl.cipher.name="TLS_AES_128_GCM_SHA256"    Search for encryption suite name
- ssl.cipher.version="TLSv1.3"    Search for encryption suite version
- ssl.version="TLSv1.3"   Search for the SSL version of the certificate
- ssl.cert.subject.cn="example.com"   Search for the common domain name of the user certificate holder
- ssl.jarm="29d29d15d29d29d00029d29d29d29dea0f89a2e5fb09e4d8e099befed92cfa"   Search for assets related to Jarm
  Fingerprint content
- ssl.ja3s=45094d08156d110d8ee97b204143db14 Find assets related to specific JA3S fingerprints

#### IP or Domain Name Related Information Search

- ip="8.8.8.8"    Search for assets related to the specified IPv4 address
  ip="2600:3c00::f03c:91ff:fefc:574a" Search for assets related to specified IPv6 address
- cidr="52.2.254.36/24"   Search for C-class assets of IP
  cidr="52.2.254.36/16"is the B class of the IP, cidr="52.2.254.36/8"is the A class of the IP, e.g.
  cidr="52.2.254.36/16"
  cidr="52.2.254.36/8"
- org="Stanford University"   Search for assets of related organizations Used to locate IP assets corresponding to
  universities, structures, and large Internet companies
- isp="China Mobile"  Search for assets of related network service providers Can be supplemented with org data
- asn=42893 Search for IP assets related to corresponding ASN (Autonomous system number)
- port=80 Search for related port assets Currently does not support simultaneous open multi-port target search
- hostname="google.com"       Search for assets of related IP "hostname"
- domain="baidu.com"  Search for domain-related assets Used to search domain and subdomain data

- banner="FTP" Search by protocol messages Used for searching HTTP response header data
- http.header="http"   Search by HTTP response header Used for searching HTTP response header data
- http.header_hash="27f9973fe57298c3b63919259877a84d"  Search by the hash values calculated from HTTP header.
- http.header.server="Nginx"   Search by server of the HTTP header Used for searching the server data in HTTP response
  headers
- http.header.version="1.2"    Search by version number in the HTTP header
- http.header.status_code="200"    Search by HTTP response status code Search for assets with HTTP response status code
  200 or other status codes, such as 302, 404, etc.
- http.body="document" Search by HTML body
- http.body_hash="84a18166fde3ee7e7c974b8d1e7e21b4"    Search by hash value calculated from HTML body

#### Fingerprint Search

- app="Cisco ASA SSL VPN" Search for Cisco ASA-SSL-VPN devices For more app rules, please refer to [object Object].
  Entering keywords such as "Cisco" in the search box will display related app prompts
- service="ssh"   Search for assets related to the specified service protocol Common service protocols include: http,
  ftp,
  ssh, telnet, etc. (other services can be found in the domain name sidebar aggregation display of search results)
- device="router" Search for router-related device types Common types include router, switch, storage-misc, etc. (other
  types can be found in the domain name sidebar aggregation display of search results)
- os="RouterOS"   Search for related operating systems Common systems include Linux, Windows, RouterOS, IOS, JUNOS,
  etc. (
  other systems can be found in the domain name sidebar aggregation display of search results)
- title="Cisco"   Search for data with "Cisco" in the title of the HTML content
- industry="government"   Search for assets related to the specified industry type Common industry types include
  technology, energy, finance, manufacturing, etc. (other types can be supplemented with org data)

- product="Cisco"  Search for assets with "Cisco" in the component information Support mainstream asset component
  search
- protocol="TCP"   Search for assets with the transmission protocol as TCP Common transmission protocols include TCP,
  UDP, TCP6, SCTP
- is_honeypot="True"   Filter for honeypot assets

#### Time Node or Interval Related Search

- after="2020-01-01" && port="50050"  Search for assets with an update time after Jan 1, 2020 and a port 50050 Time
  filters need to be combined with other filters
- before="2020-01-01" && port="50050" Search for assets with an update time before Jan 1, 2020 and a port 50050 Time
  filters need to be combined with other filters

#### Dig

- dig="baidu.com 220.181.38.148"  Search for assets with related dig content

#### Iconhash

- iconhash="f3418a443e7d841097c714d69ec4bcb8" Analyze the target data by MD5 and search for assets with related content
  based on the icon Search for assets with the "google" icon
- iconhash="1941681276"   Analyze the target data by MMH3 and search for assets with related content based on the icon
  Search for assets with the "amazon" icon

#### Filehash

- filehash="0b5ce08db7fb8fffe4e14d05588d49d9" Search for assets with related content based on the parsed file data
  Search
  for assets parsed with "Gitlab"

### Syntax Examples:

- Search for all assets of China Merchants Group in Arabic
  org="مكتب التجار الصيني" || ssl="مكتب التجار الصيني"

- Search for Starlink devices
  app=Starlink || device=Starlink

- Search for network devices running http service on port 80
  port=80 && service="http"

- Search for network devices running ssl on port 443 in Nagoya
  city=nagoya && port=443 && service=ssl

- Search for network devices running Windows operating system in the United States
  country=us && os=windows

- Search for devices running Microsoft NTP application
  app="Microsoft NTP"

- Search for webcams in Tokyo
  city=tokyo && device=webcam

- Search for industrial control devices with component 6ES7 315-2EH14-0AB0 running on port 102
  port=102 && module_id=6ES7 215-1BG40-0XB0

- Search for assets indexed after 2020-01-01 with port 50050 open
  after="2020-01-01" && port=50050

- Search for assets in Delta, Canada
  country=Canada && city=Delta

- Search for assets in Poland with Linux system and port 22
  os=linux && port=22 && country=PL

- Search for FTP service with hostname example
  service=ftp && hostname=example

- Search for IPv4 assets
  is_ipv4=true

- Search for IPv6 assets
  is_ipv6=true

- Search for IP assets containing "FreeBSD", including both IPv4 and IPv6
  FreeBSD && (is_ipv4=true || is_ipv6=true)

- Search for website assets containing FreeBSD
  FreeBSD && is_domain=true

- Search for assets with "Knownsec" in the body
  http.body="Knownsec"

- Search for specific Header hash
  http.header_hash="9763f6e29aa78e7ca2179ac82decbc25"
"""