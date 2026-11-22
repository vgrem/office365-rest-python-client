# The `o365` command line

The package installs a console script named `o365`. It is a front end to the same model the
library ships: every word it accepts and every URL it sends is read from the types, the declared
permissions and the index the generator writes — nothing here keeps a list of its own.

```bash
pip install office365-rest-python-client
o365
```

```
usage: o365 [graph|sharepoint|exchange] login|whoami|logout [flags]
       o365 <product> <noun> [navigation ...] [action] [flags]
       o365 <product> <noun> list [-o table|wide|json|csv|tsv|url|name]
       o365 <product> <noun> ... delete [--yes] [-n|--dry-run]
       o365 graph <product> <noun> [navigation ...] [action]
       o365 login [--tenant <tenant>] [--client-id <id>] [--mode device-flow] [--scopes ...]
       o365 sharepoint use <site> [--as <name>]   (a site is one ClientContext)
       o365 sharepoint context [ls|use <name>|inspect]
       o365 config [tenant|client_id|site]     (what is answered, and where from)
       o365 completion bash|zsh|fish [--warm [product ...]]
       o365 licences [-o table|wide|csv|tsv|json]
       o365 doctor [<product> <noun> [action]] [-o table|wide|json]
  a flag falls back to O365_CLIENT_ID/O365_TENANT/O365_SITE, then to ~/.o365/config.json
```

## Log in once

One token serves every command in its audience, so the first thing to do is log in:

```bash
o365 login                                          # device flow, the default
o365 login --mode client-secret --client-secret "$SECRET"
o365 login --mode username-and-password --username me@contoso.com --password "$PW"
```

`--mode` chooses the credential entry point; every other flag is a parameter that method
declares, so `o365 login -h` is the API's own signature. The modes are `device-flow`,
`interactive`, `client-secret`, `certificate` and `username-and-password`.

Two answers are not part of a mode: which application is asking, and which directory it asks.
They are read from `--client-id` / `--tenant` for one run, then `O365_CLIENT_ID` /
`O365_TENANT` for one shell, then `~/.o365/config.json` for every run. That file is yours — the
CLI only ever reads it — so it will not write it for you. Instead it prints the file it wants,
with this machine's path and the values you have already given:

```console
$ o365 login
o365: no client id yet

  Give it once, so that no command has to repeat it
  (a file you own: o365 config reads it, and never writes to it):

    mkdir -p ~/.o365
    cat > ~/.o365/config.json <<'EOF'
    {
      "tenant": "contoso.onmicrosoft.com",
      "client_id": "<application (client) id>"
    }
    EOF

  or for this shell:  export O365_CLIENT_ID=<client-id>
  or for one command: --client-id <client-id>
```

`o365 config` is the same answer as a table, which is what to run when a command behaves
differently from what you expect:

```console
$ o365 config
SETTING    VALUE                             FROM
tenant     mediadev8.onmicrosoft.com         ~/.o365/config.json
client_id  <not set>                         not set
site       https://mediadev8.sharepoint.com  derived from the tenant

file         ~/.o365/config.json   (read only: edit it yourself)
flags        --tenant, --client-id, --base-url   (one run, and they win)
environment  O365_TENANT, O365_CLIENT_ID, O365_SITE
```

`FROM` names the source, not just its kind: the path of the file that answered, `environment`,
`derived from the tenant` for the SharePoint host a `<label>.onmicrosoft.com` tenant gets by
default, or `not set`. `o365 config <key>` prints one resolved value and exits `1` when nothing
answers it, so a script reads what a command would use instead of restating the order:

```bash
client_id=$(o365 config client_id) || { echo "run o365 config to see what is missing"; exit 1; }
```

A login is a greeting, not a report — the grants are the answer to a question nobody has asked
yet, and forty-nine scope names bury the three facts worth reading at that moment:

```console
$ o365 login
To sign in, use a web browser to open the page https://login.microsoft.com/device and enter the code ABC1234 to authenticate.
logged in: graph as vadimadm@mediadev8.onmicrosoft.com (device-flow, 60 permissions, 65 min left)
  o365 whoami names the grants; o365 doctor says what this tenant allows
```

Tokens are kept in `~/.o365/sessions.json`, per audience: `o365 whoami` says who you are and
lists what the token grants (wrapped to the terminal), `o365 doctor` says what the tenant holds
and what a route needs, and `o365 logout` forgets one audience or all of them.

## The grammar

```
o365 <product> <noun> [navigation ...] [action]
```

`<product>` is one of the 22 products the index publishes (`o365 directory …`,
`o365 intune …`, `o365 outlook …`), plus the three audiences that own a token (`graph`,
`sharepoint`, `exchange`). Because 25 products share the Graph token and no package is called
`graph`, `o365 graph <product> …` is the explicit spelling of the same thing.

The rest is the route: a noun, then the links that hang off it, then what to do.

```bash
o365 directory user list
o365 outlook message list
o365 intune managed-device list
o365 onedrive drive get
```

A route that stops on a noun prints that noun's page: the verbs it answers, grouped by effect,
and the links it holds. `-h` on any route prints the flags, the permission the call declares and
the licence it needs; `o365 help <route>` asks the same question by name.

## Reading

`list` reads the feed, `get` reads one object.

```console
$ o365 directory user list
DISPLAYNAME         USERPRINCIPALNAME                                 MAIL
a.dyukov            a.dyukov_hotmail.com#EXT#@mediadev8.onmicrosoft…  a.dyukov@hotmail.com
```

| `-o` | What it prints |
| --- | --- |
| `table` | the type's own columns, values truncated to the terminal (`…` marks the cut) |
| `wide` | every field the service returned, no truncation |
| `json` | the payload as it came |
| `csv`, `tsv` | the same rows for a spreadsheet |
| `url` | one address per line, from the type's `link` fields |
| `name` | one name per line |

```bash
o365 outlook message list -o json | jq '.[].subject'
o365 directory user list --columns displayName,userPrincipalName -o csv > users.csv
```

`table`, `csv`, `tsv` and `url` ask the service only for the fields they print (`$select`); `json`
and `wide` send no `$select` at all, so a caller piping to `jq` gets the service's own payload.
With `-o csv`, `-o tsv` or `-o json` the one-sentence headline goes to stderr, keeping stdout pure
data. `--no-headers` drops the header line, and `--link auto|always|never` decides whether a name
is wrapped in a clickable hyperlink — `auto` means "only when printing to a terminal", so a pipe
never carries escape codes.

An empty feed is a sentence, not an empty table: `o365 intune managed-device list` in a tenant
with no devices prints `No managed-device found.` — and `-o json` answers `[]` there, so a pipe to
`jq` stays valid.

## Writing

A write is the same command with the method's own flags, because the flags *are* its parameters:
`o365 <route> -h` lists them along with the permission the call declares and the licence it needs.

```console
$ o365 directory group delete
o365: `delete` destroys what the service holds; send it again with --yes
```

`--yes` is added only to a command whose declared effect is `destroy` — the one that asks — so a
read never shows a flag that would do nothing. `-n` / `--dry-run` works everywhere: it prints the
request the client would send (`GET https://…`) and sends nothing, using the walk the model
already knows, so it answers with a stale token too.

## What is not here yet

A command's object has to be reachable from the client root by links the model declares. That is
what `list` and `get` do today: 98 of the index's 137 `list` routes and 265 of its 2037 `get`
routes walk from the root, and the rest are refused by name rather than guessed at.

An item *inside* a feed is not addressable from the command line yet. `EntityCollection.__getitem__`
already takes the key and `Route` already knows the feed that holds the item, but no word on the
line supplies the key, so a delete of one group answers:

```console
$ o365 directory group delete --yes
o365: directory group delete is declared, but nothing walks there from GraphClient: every link on the way needs an argument the model does not name yet
```

3601 of the index's delete and update routes end that way, and 528 reach a root link — mostly the
singleton settings objects, which have no key to give. Reads are complete for feeds; addressing
one item by key is the next gap, and the refusal above is the honest answer until it closes.

## One site at a time (SharePoint)

A SharePoint token covers every site collection, but a command runs against exactly one. The
session remembers where it is addressed, and the choice outlives the process:

```bash
o365 sharepoint use https://contoso.sharepoint.com/sites/legal --as legal
o365 sharepoint context                # where this session is, and the sites it remembers
o365 sharepoint context ls
o365 sharepoint context inspect        # the current one on its own lines
o365 sharepoint lists list -s https://contoso.sharepoint.com/sites/hr   # this command only
```

`--as` remembers the URL under a name, so `o365 sharepoint use legal` is enough afterwards. `-s`
/ `--site` (or `O365_SITE`) overrides the sticky choice for one command, and `--dry-run` prints
the absolute URL, so the site a destroy would touch is visible before it is sent.

## What you have, before you run anything

```bash
o365 licences      # which licences the commands name, and whether this tenant holds them
o365 doctor        # the session, the tenant's plans and roles, and what those plans open
o365 doctor intune managed-device retire   # what one command needs from this session
```

`licences` joins the markers the library carries to one read of the tenant's subscriptions. Each
row is a plan, the seat it is asked of (`tenant` or `user`), whether it is held, how many nouns it
opens and how many areas those nouns live in. A plan the tenant did not buy reads `no`; a seat the
token could not read reads `unknown`, never `no`.

```console
$ o365 licences
mediadev8.onmicrosoft.com: holds all 4 licences a command names

PLAN            SEAT    HELD  NOUNS  AREAS
INTUNE_A        tenant  yes     131     11
AAD_PREMIUM_P2  tenant  yes      16      4
AAD_PREMIUM_P2  user    yes       3      1
AAD_PREMIUM     tenant  yes       2      2

next: o365 licences -o wide   the areas each plan opens, by name
      o365 doctor             this session, this tenant, and what they allow
```

A list is not a table cell: `INTUNE_A` opens eleven modules, and at 48 columns that cell reads
`intune.devices (119), intune.print (3), intune.audit, intune.edition_upgrade…` — four names and
an ellipsis. So the row counts the areas by default (`AREAS 11`), and `-o wide` prints them whole
(`intune.devices (119), intune.print (3), intune.audit, intune.edition_upgrade_configuration, …`
to the last one). `-o csv` and `-o json` carry the names too, because a machine does its own
column fitting.

`doctor` answers the environment — the session and its grants, the plans and roles the caller
holds, and the index's per-product totals, which need no session at all — in four requests:

```console
$ o365 doctor
doctor: ok — 1 session, 4 of 4 licences, 12 roles

graph: mdoe@mediadev8.onmicrosoft.com (tenant af6a80a4-8b4b-4879-88af-42ff8a545211, mode username-and-password, 55 min left)
  grants: 55 scopes

mediadev8.onmicrosoft.com: holds all 4 licences a command names
  roles: 12 held — Application Administrator, Compliance Administrator, Exchange Administrator,
         Global Reader, Groups Administrator, Intune Administrator, Search Administrator, Security
         Administrator, SharePoint Administrator, SharePoint Embedded Administrator, Teams
         Administrator, User Administrator

PLAN            SEAT    HELD  NOUNS
INTUNE_A        tenant  yes     131
AAD_PREMIUM_P2  tenant  yes      16
AAD_PREMIUM_P2  user    yes       3
AAD_PREMIUM     tenant  yes       2

PRODUCT    NOUNS  LICENSED
directory    423        21
intune       362       131
no licence is named under the other 20 products (1,252 words); -o wide lists them

next: o365 licences -o wide              every licence, and the areas it opens
      o365 doctor <product> <noun> ...   what one command needs from this session
```

The page opens with the answer, because that is why it was opened: `attention` when a command
would refuse right now (no session, or one that expired — with the command that renews it),
`unread` when a fact could not be read (which is not an accusation), and `ok` with the three
numbers it read. `gh auth status` and `flutter doctor` lead the same way; a page that ends with
the verdict makes a reader scan everything to find it.

After the verdict, three blocks in the order a reader needs them: are my sessions alive, does
this tenant hold what the commands ask, and which products name a licence at all. `-o wide`
prints the row that a table would have to shorten — the families each plan opens (`intune.devices
(119), intune.print (3), …`) — and the products that name no licence; both belong to the report,
not to the moment before a first command.

Given a route it answers instead for one command, with no request to the service being asked
about: the delegated and application permissions the method declares, marked against the token's
own `scp`/`roles`, the licence the type names, and one row per directory role it asks for. `have`,
`missing` and `unknown` are the same three words as above.

## Completion

```bash
o365 completion bash >> ~/.bashrc      # zsh and fish work the same way
o365 completion --warm                 # fill the cache so a TAB never pays an import
```

The script asks a hidden subcommand, which answers from the index and the model's own metadata —
the command line's words first (products, session verbs, flags), the model's nouns second. It
never sends a request, and `--warm` writes the cache once so that a later TAB reads it back.

## Exit codes and environment

| Code | Meaning |
| --- | --- |
| `0` | the command ran, or the question was answered |
| `1` | the service refused the request; its own words are printed |
| `2` | nothing ran: unknown word, unreadable flag, missing session, or a destroy without `--yes` |

| Variable | Means |
| --- | --- |
| `O365_TENANT`, `O365_CLIENT_ID` | the defaults `--tenant` / `--client-id` fall back to; `o365 config` prints which one answered |
| `O365_SITE` | the site a SharePoint command is addressed at |
| `O365_HOME` | where `sessions.json` and `config.json` live (default `~/.o365`) |
| `O365_CACHE` | the completion cache (default `~/.cache/o365/completion.json`) |
