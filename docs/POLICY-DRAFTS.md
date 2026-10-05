# Privacy policy and terms: changes for photo uploads

The connector can now receive the user's own photos (`upload_image`, `create_upload_link`), which
the current privacy policy (updated 03.10.2026) rules out: "We do not receive your conversation,
files you upload to the assistant, or anything else from your account there." Publish these changes
before plugin 1.0.2 goes out, so the plugin README and the policy say the same thing.

Facts behind the text, from `pin-generator-tool` at #88: uploads are JPEG, PNG or WebP; the server
turns the image upright and drops EXIF, GPS, XMP and IPTC data; it stores the result in Cloudflare R2
at a random address for 7 days; an upload link works once, for 15 minutes; the default limit is 30
uploads per account per day; `mcp_uploads` keeps a record of every upload (time, size, format,
dimensions, how it was uploaded, a hash of the link token) after the image is deleted; the server
logs each upload with the account ID.

Two parts are marked [check]: confirm them against your storage setup and your intentions before
publishing, and remove the brackets.

## Privacy policy

### In "The InsightPins connector for Claude", replace the last sentence of "What the assistant sends us"

Old:

> We do not receive your conversation, files you upload to the assistant, or anything else from your
> account there.

New:

> We do not receive your conversation, files you share with the assistant, or anything else from your
> account there, unless you ask the assistant to put one of your own photos on a pin (see "Uploaded
> photos").

### Add after "Pages and images"

> - **Uploaded photos.** When you want one of your own photos on a pin, the assistant uploads it to
>   us, or gives you a link to a page where you upload it yourself (the link works once, for 15
>   minutes). We accept JPEG, PNG and WebP images. Before storing a photo we turn it upright and
>   remove the information a camera or phone adds to it, including its location, the device and the
>   time it was taken. We store the photo with Cloudflare R2 at a random, unguessable address, so the
>   pin can be drawn; anyone who has that link can open it. It is deleted 7 days after you upload it
>   [check: "(deletion can run up to a day later)", as for rendered pins]. We do not use your photos
>   for anything else [check: and we do not use them to train AI models, if that is your commitment].
> - **Upload records.** For each upload we keep the time, the image size, format and dimensions, and
>   whether it came from the assistant or the upload page. We use them to count your daily upload
>   limit, and they stay for as long as your account does. They do not contain the photo.

### In "Server logs", add uploads

Old:

> Our server also logs when you connect an app, and any page fetch or render that fails, together
> with your account ID; a failure can include the page or image URL.

New:

> Our server also logs when you connect an app, each photo you upload (its size and format), and any
> page fetch, upload or render that fails, together with your account ID; a failure can include the
> page or image URL.

### Optional, in "5. Data Retention and Security"

> - **Photos you upload through the connector** are deleted 7 days after upload; the record of the
>   upload (without the photo) stays with your account.

Update "Last Updated" when you publish.

## Terms of use

### In "1. The Services", the connector paragraph

Old:

> It is free and limited to 50 rendered pins per account per day, reset at 00:00 UTC. Download links
> to rendered pins work for 7 days.

New:

> It is free and limited to 50 rendered pins and 30 uploaded photos per account per day, reset at
> 00:00 UTC. Download links to rendered pins and uploaded photos work for 7 days.

### After "You are responsible for having the right to use the text and images you put on a pin..."

> This includes photos you upload: only upload photos you took yourself or have permission to use,
> and if a photo shows other people, make sure they are happy for it to be published. You keep all
> rights to your photos. By uploading one you allow us to store it and use it to draw your pins until
> it is deleted 7 days later, and for nothing else.

## Where else the change shows

- Plugin README, "Data handling": updated in the same pull request as plugin 1.0.2.
- Developer portal, plugin data handling: the retention answer gains "uploaded photos 7 days"
  (see `SUBMISSION.md`).
- Connector listing: the description now lists 8 tools, and the data handling step should say the
  connector receives photos the user chooses to upload, which may show people.
