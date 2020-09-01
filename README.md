# blog-backend-flask

Blog REST API on Flask

see [blog-frontend-vuejs](https://github.com/qbbr/blog-fontend-vuejs)

## depends

 * [python3](https://www.python.org/)
 * see [requirements.txt](requirements.txt)

## run

```bash
python3 -m venv venv
 . venv/bin/activate
pip install -r requirements.txt
. .env.dev
flask init-db
flask run
```

## routes

| route               | method     | description                      | JWT required |
|---------------------|------------|----------------------------------|--------------|
| /register/          | POST       | create new user                  |              |
| /login/             | POST       | login                            |              |
| /user/profile/      | GET        | get user profile                 | Y            |
| /user/profile/      | PUT, PATCH | update user profile              | Y            |
| /user/profile/      | DELETE     | delete user profile              | Y            |
| /posts/             | GET        | get all posts \w pagination      |              |
| /post/{slug}/       | GET        | get post by slug                 |              |
| /tags/              | GET        | get all tags                     |              |
| /user/posts/        | GET        | get all user posts \w pagination | Y            |
| /user/posts/        | DELETE     | delete all user posts            | Y            |
| /user/post/         | POST       | create user post                 | Y            |
| /user/post/{id}/    | GET        | get user post by id              | Y            |
| /user/post/{id}/    | PUT, PATCH | update user post by id           | Y            |
| /user/post/{id}/    | DELETE     | delete user post by id           | Y            |
| /user/post/md2html/ | POST       | convert markdown to html         | Y            |

## tests

nope, need to write ;)
