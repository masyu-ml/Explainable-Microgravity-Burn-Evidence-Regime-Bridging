# Repository Source Status

**Important distinction:** This GitHub documentation does not claim to contain the complete latest source of the deployed EMBER website.

The full GitHub-ready ZIP assembled previously from recovered project archives contains an earlier **V2 scientific-core snapshot**, an **archived V5 BASS-II evidence pipeline**, and a **legacy v1.3 console**. Those packages differ from the live, more recent Vercel application with additional UI, voice, audit and physics patches.

The available GitHub connector could publish text files, but it did not directly import the prepared ZIP as a Git source tree. The files currently committed here are documented code extracts, an independent runnable retrieval example, and research documentation. **Do not treat them as a 1:1 production deployment.**

Live site: https://ember-mvp-one-man-orbit.vercel.app/

## Separation of concerns

- **Vercel:** preserved unchanged; no production edits are authorized by this publishing task.
- **GitHub:** documentation, examples, model explanation and source snapshots may be updated independently.
- **Scientific provenance:** experimental evidence, code calculations and uncertainty remain distinguished.
- **Completeness:** do not present an incomplete reconstruction as the complete live application.

To create an exact production source mirror, export the current Vercel source from the original development workspace and audit the dependency tree, configuration, secrets and file hashes before committing it.
