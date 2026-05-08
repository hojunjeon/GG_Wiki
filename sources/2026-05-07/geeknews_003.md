---
source: geeknews
date: 2026-05-07
points: 9
url: "https://developers.cloudflare.com/changelog/post/2026-05-06-react-nextjs-vulnerabilities/"
title: React 및 Next.js에서 다수의 보안 취약점 공개, 즉시 패치 권고
---

# React 및 Next.js에서 다수의 보안 취약점 공개, 즉시 패치 권고

WAF and framework adapter mitigations for React and Next.js vulnerabilities
Multiple security vulnerabilities were disclosed by the React team and Vercel affecting React Server Components and Next.js. These include denial of service, middleware and proxy bypass, server-side request forgery, cross-site scripting, and cache poisoning issues across a range of severity levels.
We strongly recommend updating your application and its dependencies immediately. Patched versions are available for React (react-server-dom-webpack
, react-server-dom-parcel
, and react-server-dom-turbopack
19.0.6
, 19.1.7
, and 19.2.6
) and Next.js (15.5.16
and 16.2.5
).
Cloudflare WAF rules deployed in response to prior React Server Component CVEs (CVE-2025-55184
↗ and CVE-2026-23864
↗) already provide coverage for the newly disclosed denial-of-service vulnerabilities. These rules are enabled by default with a Block action for all customers using the Cloudflare Managed Ruleset, including Free plan customers using the Free Managed Ruleset.
The existing rules detect the underlying attack patterns generically. As a result, they apply to the new CVE-2026-23870
↗ denial-of-service vulnerability in Server Components and the corresponding Next.js advisory GHSA-8h8q-6873-q5fj
↗.
Cloudflare is investigating whether WAF rules can be safely and effectively deployed for three of the high-severity advisories: CVE-2026-23870
↗ / GHSA-8h8q-6873-q5fj
↗, GHSA-267c-6grr-h53f
↗, and GHSA-mg66-mrh9-m8jx
↗. If it is possible to create a managed WAF rule that mitigates these CVEs and does not potentially break application behavior, Cloudflare will add additional managed WAF rules. These rules will be announced through the WAF changelog. Because these vulnerabilities were shared with Cloudflare with minimal advance notice, we are still investigating what WAF mitigations are possible.
Several of the disclosed vulnerabilities are not possible to block in WAF. We strongly recommend updating your applications so they are not purely reliant on WAF mitigations.
Customers on Pro, Business, or Enterprise plans should ensure that Managed Rules are enabled.
Vinext: Vinext ↗ is a Vite plugin that reimplements the Next.js API surface. Vinext's latest release is not vulnerable to any of the disclosed CVEs. Vinext's architecture differs from stock Next.js in ways that sidestep the affected code paths. For example, it does not implement the PPR resume protocol, does not expose Pages Router data-route endpoints, and strips internal headers such as x-nextjs-data
at request boundaries. As an extra layer of defense, we added a React 19.2.6
or later requirement when running vinext init
(PR #1118 ↗, PR #1112 ↗) to prevent accidentally running a vulnerable version of React with Vinext.
OpenNext on Cloudflare: OpenNext is an adapter that lets you deploy Next.js apps to the Cloudflare Workers platform. OpenNext itself is not directly vulnerable to the React denial-of-service CVE, but users must update the Next.js version in their application. The OpenNext team has updated the adapter to further harden against these vectors and released a new version of the Cloudflare adapter. Test fixtures and examples have been updated to use patched versions (PR #1255 ↗).