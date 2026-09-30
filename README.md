# review-demo-exporter

Test fixture for evaluating a code-review tool. Not production code.

Exports notes to JSON. Each note has exactly four fields:

| field        | type   |
|--------------|--------|
| `id`         | int    |
| `title`      | string |
| `body`       | string |
| `created_at` | ISO-8601 UTC string |

Downstream: [review-demo-consumer](../review-demo-consumer) reads this output.

```bash
python -m exporter.notes_export            # print to stdout
python -m exporter.notes_export out.json   # write to file
python -m unittest -v                      # run tests
```
