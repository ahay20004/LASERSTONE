# LASERSTONE Hugging Face Spaces — controlled static preview

**No Space has been created or deployed by this repository change.** Owner approval and a Hugging Face account are required.

## Why static first
The initial preview contains only approved bilingual informational HTML/CSS/JS. Gradio and Python compute are deferred until scientific validation, authentication boundaries and quotas are reviewed. Hugging Face public Spaces must be treated as publicly accessible; do not place owner dashboard, credentials, private data or patent-enabling confidential details there.

## Prepare
1. From the repository root run `python -m unittest -v cloud/test_preview_static.py`.
2. Run `python cloud/huggingface/prepare_space.py --output <EMPTY_STAGING_DIRECTORY>`.
3. Review every staged file and the README metadata. Confirm ownership, licensing, trademarks and patent disclosure clearance.
4. In the owner's Hugging Face account, create a **Static** Space with a chosen unique name and visibility after reviewing public disclosure implications.
5. Upload the staged files into the Space repository root using the Hugging Face UI or a separately authenticated git push. Never commit tokens to GitHub or this Space.
6. Open the resulting Space URL and test Arabic/English, RTL, keyboard navigation, mobile layout and actual response headers.
7. Record Space URL, revision, test evidence, and explicit owner approval in a private release log.

## Hosting differences and limitations
- `cloud/site/_headers` is a Cloudflare Pages configuration and is intentionally NOT copied to the Space. Do not claim its CSP or other HTTP headers are active on Hugging Face.
- Do not claim live visitor counts, owner authentication, private access or production scientific engines.
- The static preview does not collect accounts or feedback; analytics require a separately reviewed privacy and hosting design.
- Free-tier availability, resource limits, provider policy and uptime must be checked at deployment time.
- Keep the GitHub development PR unmerged until reviewed; do not enable automatic publication from an unreviewed branch.
- Public release may affect patent novelty. Seek qualified IP review before making implementation details public.

## Future interactive phase
A separate Gradio Space may host bounded, **synthetic** examples after reviewing input validation, compute limits, abuse protection and reproducibility. Sensitive research workspaces and the owner cockpit require a separate secured service with server-side authorization.
