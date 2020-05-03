# Boardgame finder

## Crawling

```shell script
mkdir data
python -m crawler
aws s3 sync data/ s3://YOUR_BUCKET/boardgame_finder/
```

This crawling script is idempotency.

If your assertion error, open your browser -> google captcha and restart script

## Parsing

```shell script
python -m meta_parser
```

Generated `boardgame_meta.json` 
