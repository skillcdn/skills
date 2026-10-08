# Cast images

Every person in the ad has an approved portrait, and every generated shot an approved still first frame. The method every Higgsfield skill shares (which image models and how they are found, the style line, the portrait prompt, the approval loop, how a frame becomes a take, reuse by id) is in [/docs/higgsfield/cast.md](/docs/higgsfield/cast.md); this page is what the ad adds: who is cast, where a face may come from, and what the shot list keeps.

## Who needs a portrait

One portrait per cast member in the shot list: the people named in the brief's "Cast" section, rewritten in phase 3 for the user's product and for what must differ. A voice-over, or a speaker who stays outside the frame, needs no portrait; the frame prompt says that this person is not visible (a back, a shoulder, or nothing), so that the model invents no second face. A product is not a cast member; it appears through the product site's images, a user-supplied image or an overlay, as [editing-decisions.md](editing-decisions.md) says.

Nothing from the reference video is used for a portrait: not a frame, not a crop, not a description that names one of its people, even when the reference shows the same persona as the product's site. A portrait never shows a real person or a celebrity likeness, a logo on clothing, or text.

## The product's own people

A person the product's own site presents (its founder, its face, a mascot) is the advertiser's own asset and may be cast when the composition calls for it. Their site photo, imported with `media_import_url`, is then the portrait itself; when the plan wants a different look (period clothing, a setting) or the ad is animated (the person drawn in the style line from the photo), the image model makes the portrait with that photo as its reference input, and the user approves it like any other. The plan checkpoint says whether a site person appears. When the reference is an earlier ad of the same product and shows that persona, the persona is still cast from the site's photo and the plan's description, never from the reference's frames.

## In the ad's medium

The image models follow the brief's medium: for live action, the identity model from a text description; for an animated or stylized reference, the reference-capable model with the style line, which makes the portraits and the first frames alike. Each is found at run time with `models_explore` (`recommend`, type `image`, a query in words of what it must take and make; the shared page has the queries), locked at its cheapest setting and preflighted once. A first frame carries the shot's starting emotion and the product image where the product appears; the take prompt carries the turn. For animation the take prompt says that this is a drawn, animated scene whose style holds throughout, so the model does not drift toward photoreal.

## What the shot list keeps

The approved portrait's media id or job id, and the words the portrait settled (its clothing and the two or three most identifying traits, repeated in every frame and take prompt for that character). A later run for the same brand can reuse an approved portrait instead of generating a new one: offer it, and let the user decide.
