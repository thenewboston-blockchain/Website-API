## Overview

REST API for thenewboston.com.

## Project Setup

Follow the steps below to set up the project on your environment. If you run into any problems, feel free to leave a 
GitHub Issue or reach out to any of our communities above.

Install required packages:
```
pip3 install -r requirements/local.txt
```

## Developers

When adding a package, add to `requirements/base.in` and then:
```
bash scripts/compile_requirements.sh
```

To run tests:
```
pytest
```

To check styling:
```
flake8 --config=.flake8 config tests v1
```

## Community

Join the community to stay updated on the most recent developments, project roadmaps, and random discussions about 
completely unrelated topics.

- [thenewboston.com](https://thenewboston.com/)
- [Slack](https://join.slack.com/t/thenewboston/shared_invite/zt-hkw1b98m-X3oe6VPX6xenHvQeaXQbfg)
- [reddit](https://www.reddit.com/r/thenewboston/)
- [LinkedIn](https://www.linkedin.com/company/thenewboston-developers/)
- [Facebook](https://www.facebook.com/TheNewBoston-464114846956315/)
- [Twitter](https://twitter.com/bucky_roberts)
- [YouTube](https://www.youtube.com/user/thenewboston)
