# Guarded Instagram publishing with n8n

This guide describes a self-hosted publishing queue. It is not a claim that any social account is connected or that posts have been published.

## Components

- n8n stable2.47.7, Node24, PostgreSQL16 compatibility mode. PostgreSQL17+ is the supported upgrade target; do not change an existing shared cluster as a side effect of setup.
- Loopback editor and queue bridge. Separate editor and task-broker ports: using5679for both causes startup failure.
- Queue rows contain an approved account, format, publish time, immutable assetSHA256, caption, exactlyfive hashtags and a music declaration.
- Count two broad discovery tags and three topic tags. No hashtag guarantees virality.
- A narration track is not background music. A file may contain an original/user-owned score; otherwise require a verified Instagram catalog track before publication.
- Meta supports the Instagram Audio API through Facebook Login. A browser login is not an API access token. Keep credentials in n8n encrypted storage or protected environment files, never workflow exports.
- For Reels, use createcontainer→pollprocessing→publish→verifypermalink. Record a durable STARTED state before external writes. An uncertain outcome requires inspection, not an automatic re-upload.
- NativeSafariweb uploads can require a real file-picker event and accessibility AXPress. A synthetic file assignment may show a file while never running the active upload handler. Keep the owned task tab visible; verify a real video preview before publishing.
- macOSLaunchAgents should run from an application/project directory. Desktop/iCloud access can require user privacy permissions; do not grant FullDiskAccess just to read generated runtime assets. Retain user-facing originals and put the approved service copies in the project runtime directory.

## Validation

Check missing-token and missing-media-URL holds, exact hashtag count, missing-music hold, allowed format, duplicate/uncertain states, health endpoints and a manual n8n workflow execution. Preparing a queue is not platform scheduling. Running n8n is not a connected Instagram publisher.

## Handoff checklist

Record actual published links separately from drafts, queued jobs and uncertain attempts. Include runtime paths, workflowID/version, last successful execution, asset hashes, service/port configuration, primary references and the next concrete action. Exclude tokens,passwords,keys and private customer data.

References:
- https://github.com/n8n-io/n8n
- https://docs.n8n.io/hosting/cli-commands/
- https://developers.facebook.com/documentation/instagram-platform/changelog
- https://developers.facebook.com/docs/instagram-platform/content-publishing/audio-api
- https://github.com/facebook/facebook-python-business-sdk/blob/main/facebook_business/adobjects/iguser.py
