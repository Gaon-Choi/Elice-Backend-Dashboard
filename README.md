# Elice-Backend-Dashboard

## Project Outline
본 프로젝트에서는 간단한 게시판 서비스를 구축하기 위한 API를 담고 있다.

유저 정보를 이용하여 로그인 및 로그아웃 기능을 기반으로 게시판과 게시글 작성, 삭제, 수정 등에 적절한 권한 설정을 적용한다.

대시보드에는 여러 개의 게시판이 존재할 수 있으며, 유저로 로그인하여야 새로운 게시판을 만들거나 삭제할 수 있다.

하나의 게시판에는 다수의 게시글이 작성될 수 있다. 각각의 게시글을 읽는 것에는 별도의 권한 조건이 없으나, 특정 게시글을 삭제하거나 수정하는 작업은 해당 게시글을 작성한 유저만 수행할 수 있도록 권한을 설정한다.

## Design
### Schematic Design
본 프로젝트에서 사용한 테이블 디자인입니다. 컬럼명에 굵은 글씨로 표시된 것은 Primary Key를 나타내며, 밑줄 형태로 표시된 것은 Foreign Key를 나타냅니다.

1. 사용자 테이블 users

|column name|data type|detail|
|------|---|---|
|**id**|Integer|사용자 식별 id|
|name|Character(30)|사용자 이름|
|email|Character(50)|사용자 이메일 (중복불가)|
|password|Character(80)|사용자 패스워드 (SHA 적용)|

2. 게시판 테이블 boards

|column name|data type|detail|
|------|---|---|
|**id**|Integer|게시판 식별 id|
|name|Character(30)|게시판 이름|

3. 게시글 테이블 articles

|column name|data type|detail|
|------|---|---|
|**id**|Integer|게시글 식별 id|
|<U>board_id</U>|Integer|소속 게시판 id: boards.id|
|title|Character(100)|게시글 제목|
|contents|Text|게시글 내용|
|<U>writer</U>|Integer|작성 유저 id: users.id|
|date|Timestamp with time zone|게시글 생성일|
|edate|Timestamp with time zone|게시글 수정일 (최신)|
|status|Boolean|게시글 삭제 여부|

## REST API Specification
아래는 유저, 게시판, 게시글, 대시보드에 대한 API 설명을 담고 있다.
모든 API는 응답으로 JSON 형식을 전송하며 "result"와 "status"의 두 개의 키를 가지고 있다. 이는 각각 요청에 대한 결과와 상태 코드를 나타낸다.

### User

1. 사용자 가입 기능
- endpoint: `POST /user/signup HTTP/1.1`
- body: { "name", "email", "password" }
- request body example
  ```json
  {
      "name": "gaonchoi",
      "email": "x@gmail.com",
      "password": "12345678"
  }
  ```
- response

  1) 이메일 형식이 잘못된 경우
  ```json
    {
      "result": "invalid email address",
      "status": 400
    }
  ```

  2) 중복된 이메일로 기가입자가 존재하는 경우
  ```json
    {
      "result": "duplicate email detected",
      "status": 400
    }
  ```

  3) 유저 가입이 성공적으로 이뤄진 경우
  ```json
    {
      "result": {
        "fullname": "gaonchoi",
        "email": "x@gmail.com"
      },
      "status": 201
    }
  ```

2. 사용자 로그인 기능
- endpoint: `POST /user/login HTTP/1.1`

- body: { "name", "email", "password" }

- request body example
  ```json
  {
      "name": "gaonchoi",
      "email": "x@gmail.com",
      "password": "12345678"
  }
  ```

- response

  1) 이미 로그인된 경우
  ```json
  {
    "result": "A user already logged in.",
    "status": 200
  }
  ```
  2) 이메일 형식이 잘못된 경우
  ```json
  {
    "result": "email address has invalid form.",
    "status": 400
  }
  ```
  3) 가입 정보가 존재하지 않는 경우(이메일 기반)
  ```json
  {
    "result": "User does not exist with given e-mail address",
    "status": 200
  }
  ```
  4) 입력된 비밀번호가 틀린 경우
  ```json
  {
    "result": "Wrong password!",
    "status": 401
  }
  ```
  5) 로그인에 성공한 경우
  ```json
  {
    "result": {
      "userId": "gaonchoi",
      "userEmail": "x@gmail.com"
    },
    "status": 200
  }
  ```

3. 사용자 로그아웃 기능
- endpoint: `POST /user/logout HTTP/1.1`

- body: (None)

- response

  1) 로그인 상태가 아닌 경우
  ```json
  {
    "result": "No user logged in",
    "status": 401
  }
  ```
  2) 로그아웃이 성공적으로 이뤄진 경우
  ```json
  {
    "result": "Logged out successfully",
    "status": 200
  }
  ```

### Board

1. 게시판 추가 기능
- endpoint: `PUT /board/:board_name HTTP/1.1`

  e.g. `PUT /board/notice`

- body: (None)

2. 게시판 목록 조회 기능
- endpoint: `GET /boardlist?page={page} HTTP/1.1`

  e.g. `GET /boardlist?page=1`

- body: (None)

3. 게시판 이름 변경 기능
- endpoint: `PATCH /board/:board_name HTTP/1.1`

  e.g. `PATCH /board/notice`

- body: { "target_name" }

- request body example
  ```json
    {
      "target_name": "only-for-members"
    }
  ```

4. 게시판 제거 기능
- endpoint: `DELETE /board/:board_name HTTP/1.1`

  e.g. `DELETE /board/notice`

- body: (None)

5. 게시판 글 목록 조회 기능
- endpoint: `GET /board/:board_name?page={page} HTTP/1.1`

  e.g. `GET /board/notice?page=2`

- body: (None)

### Article

1. 게시글 생성 기능
- endpoint: `POST /article HTTP/1.1`

- body: { "title", "contents", "board_name" }

- request body example
  ```json
  {
    "title": "[NOTICE] For the new users!",
    "contents": "The best thing about the future is that it comes one day at a time.",
    "board_name": "notice"
  }
  ```

2. 게시글 조회 기능
- endpoint: `GET /article/:article_id HTTP/1.1`

  e.g. `GET /article/23 HTTP/1.1`

- body: (None)

3. 게시글 제목 및 내용 변경 기능
- endpoint: `PUT /article HTTP/1.1`

- body: { "article_id", "title", "contents" }

- request body example
  ```json
  {
    "article_id": 23,
    "title": "[NOTICE] For the new users!",
    "contents": "The best thing about the future is that nobody knows it.",
  }
  ```

4. 게시글 제거 기능 (사용자)
- endpoint: `PATCH /article/:article_id HTTP/1.1`

  e.g. `PATCH /article/23 HTTP/1.1`

- body: (None)

5. 게시글 제거 기능 (관리자)
- endpoint: `DELETE /article/delete/:article_id HTTP/1.1`

  e.g. `DELETE /article/23 HTTP/1.1`

- body: (None)

### Dashboard

1. 최근 게시글 조회
- endpoint: `GET /article/recent/:rpp HTTP/1.1`

  rpp: 한 게시판 별로 조회할 게시글의 개수

  e.g. `GET /article/recent/15 HTTP/1.1`

- body: (None)

## How to Run

1. 해당 레포지토리를 로컬에 복사한다.
```
git clone https://github.com/Gaon-Choi/Elice-Backend-Dashboard.git
```

2. 레포지토리 내에서 가상 환경을 구성한 후 활성화합니다.
```
cd Elice-BackEnd-Dashboard
python -m venv venv
venv\Scripts\activate.bat
```

3. 필요한 패키지를 pip을 통해 설치한다.
```
pip install -r requirements.txt
```

4. Docker 환경에서 컨테이너를 실행한다. Docker Desktop에서 컨테이너를 직접 실행할 수 있다.
```
docker-compose up -d
```

5. app.py를 실행한다. Docker Desktop에서 "Open in VSCode"를 통해 Visual Studio Code 환경에서 실행할 수도 있다.
```
python app.py
```

6. 테스트는 Postman으로 진행하였다. Postman을 실행한 후 API Specification을 참고하여 request를 보내고 response를 확인할 수 있다.
<img src="/docs/postman.png" width="700" height="350">
