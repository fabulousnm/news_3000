# Full screenshot prompts with template references

The unified CSV contains ordinary image-generation prompts for complete
screenshots. Image+text and long prompt rows include a matching local template
image in `ui_reference_image`. Short prompts have no attached template image;
they name the exact platform and ask for a 1:1 recreation. Prompts describe the
specific template, its gray text and image placeholders, and the supplied
visible content. The generation flow does not create separate media-only tasks
or composite a screenshot afterward.

Regenerate the CSV with:

```powershell
python src/generate.py
```

Then pass `final/news_rumor_prompts_unified.csv` directly to
`batch_imagegen2.py`. Publication times and interaction counts stay from the
CSV. Device time and battery are provided as generated values only for templates
that display those fields; fictional comments have distinct accounts and copy,
with their own IP location, time, and likes. The Douyin comments prompt supplies
a title-related blue search phrase. Douyin video prompts fill the bottom search
box with a short, story-related phrase in white. CNN's upper-right and AP News'
right-side gray ad placeholders are designated for Ads images.

Long prompts keep the combined body in one coherent post-body section, use a
separate blue hashtag strip, and respect template-specific text limits.
