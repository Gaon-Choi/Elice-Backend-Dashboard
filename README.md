# Elice-Backend-Dashboard

## Project Outline
본 프로젝트에서는 간단한 게시판 서비스를 구축하기 위한 API를 담고 있다.

유저 정보를 이용하여 로그인 및 로그아웃 기능을 기반으로 게시판과 글 작성, 삭제, 수정 등에 적절한 권한 설정을 적용한다.

대시보드에는 여러 개의 게시판이 존재할 수 있으며, 유저로 로그인하여야 새로운 게시판을 만들거나 삭제할 수 있다.

하나의 게시판에는 다수의 글이 작성될 수 있다. 각각의 글을 읽는 것에는 별도의 권한 조건이 없으나, 특정 글을 삭제하거나 수정하는 작업은 해당 글을 작성한 유저만 수행할 수 있도록 권한을 설정한다.

## Design


## REST API Specification
아래는 유저, 게시판, 글에 대한 API 설명을 담고 있다.
모든 API는 응답으로 JSON 형식을 전송하며 "result"와 "status"의 두 개의 키를 가지고 있다. 이는 각각 요청에 대한 결과와 상태 코드를 나타낸다.

### User

1. 사용자 가입 기능
- endpoint: `POST /user/signup HTTP/1.1`
- body: { "name", "email", "password" }
- request body example
  ```json
  {
      "name": "chulsoo",
      "email": "chulsoo@naver.com",
      "password": "chl10280"
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
        "fullname": user_name,
        "email": user_email
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
      "name": "chulsoo",
      "email": "chulsoo@naver.com",
      "password": "chl10280"
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
      "userId": user_id,
      "userEmail": user_email
    },
    "status": 200
  }
  ```

3. 사용자 로그아웃 기능
- endpoint: `POST /user/logout HTTP/1.1`

- body: (없음)

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

2. 게시판 목록 조회 기능

3. 게시판 이름 변경 기능

4. 게시판 제거 기능

5. 게시판 글 목록 조회 기능


### Article

1. 글 생성 기능

2. 글 조회 기능

3. 글 제목 및 내용 변경 기능

4. 글 제거 기능 (사용자)

5. 글 제거 기능 (관리자)

## How to Run
