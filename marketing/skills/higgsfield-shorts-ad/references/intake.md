# Intake: what is asked, and the product brief

The artifact of phase 1 is the intake record: the two inputs, the product brief below, and every derived setting.

## What is asked

Ask only for what the request did not give and what cannot be found:

1. The product: a link to its site or page, or a name and one sentence about it.
2. The reference video: a link straight to a media file, or a local file through the upload widget where the client has one. An agent with a shell and no widget uploads a local file itself, and an unattended agent asks for a hosted link, as [/docs/higgsfield/sandbox.md](/docs/higgsfield/sandbox.md) "Files in" says. A YouTube link alone is not enough: it feeds the scene analysis but not the frames or the transcript. Short is better; analysis accuracy drops with length. When the request has none, it is found before it is asked for ([finding-a-reference.md](finding-a-reference.md)), and asked for only when nothing at hand can find one.

The message is short: the one or two things needed (for the reference, that the link must lead straight to a media file), one line on what happens next (the reference is analyzed, then a plan with its cost is shown), and nothing else. Never ask about language, length, captions, cast, setting, images or budget: those are derived and shown at the plan checkpoint, where the user can change any of them. When the request already has both, there is no intake message at all.

## Product brief

From the product page (or the user's sentence), record:

- Name, what it is, who it is for: one line each.
- The tagline, if any, verbatim.
- The claims the page makes, as a short list. Only these, or what the user states, may be spoken in the ad.
- The page's language, which becomes the dialogue and caption language: a site with several languages gives the user's where it has it (fetch with `Accept-Language` set to it and read the page's `lang`), else its default.
- The page's type and colors: font families from its stylesheet, a web font's link, the ground, text and accent colors, the logo's clear space where the site states one, else the logo's own height on every side. When the site shows two marks (the header's and the favicon), the header's is the logo.
- Images: the logo, one product image, and the photo of any person the site presents as the brand's own (a founder, a face of the brand, a mascot). Fetch the page in the sandbox (`curl -sL '<url>'`, then the linked CSS), read the `og:image` tag and the `img` sources whose path, alt or class mentions logo, product, hero, portrait or the product's name; download the candidates, look at them, and keep what serves: a logo for the end card and overlays, a product image for overlays and as a product reference where the video model takes one, a person's photo for casting. Import them with `media_import_url`, to use as they are or as references; nothing is taken from any other site.

The sandbox's own curl returns the whole page text, so a separate web-reading tool is needed only for a script-rendered page. Without the sandbox and without a web tool, ask the user for two lines about the product and go on without images.
