# Contributing

The project currently does not use Conventional Commits or any specific conventions.
Work is branched
and merged from [main](https://github.com/algorandfoundation/devportal/tree/devrel-content) as the main trunk.

For the internal devrel guide,
see the [Solas documentation](https://solas.algorand.foundation/doc/content-development-workflow-dPylBlDwdm#h-feature-branches)

## Get Started

### Setup Repository

Clone the repository if it has not been done already.
This only has to be done once to set up the project

```bash
git clone git@github.com:algorandfoundation/devportal-code-examples.git
```

Update the latest changes from the remote repository

```bash
git fetch
```

#### Feature branches

Please use the following convention when naming branches for clarity:

```
{feat/fix/chore/change}/topicgroup-section-page
```

For example:

```bash
git checkout feat/python-inner-transaction
```

### Submitting Changes

Provide a descriptive commit message that outlines the changes.
Changes must be done via a Pull Request (PR).

Ensure the following acceptance criteria are met before submitting a PR:

- Ensure there are no typos in the content
- Ensure `pnpm run lint` passes
- Ensure `pnpm run build` passes

## Code example guidelines

### RemoteCode astro component
All code examples in this repository are imported into the devportal using the `RemoteCode` [astro component](https://github.com/algorandfoundation/devportal/blob/main/src/components/RemoteCode.astro). Refer to [this PR](https://github.com/algorandfoundation/devportal/pull/75) to learn how to use the component.

Each code example MUST be wrapped with the comment that follows this standard: `example: {SECTION_NAME}`

For example:
```python
# example: LALA
I will be extracted! 👍
# example: LALA
```

## Repository structure
Code examples are divided into sub-projects in the `projects` directory depending on their type. For example, if the code example concerns an Algorand Python smart contract, it should go into the `python-contract-examples` sub-project directory.

Refer to `CONTRIBUTING.md` files in respective sub-projects in the `projects` directory for sub-project specific instructions.
