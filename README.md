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


2. 사용자 로그인 기능
- endpoint: `POST /user/login HTTP/1.1`

3. 사용자 로그아웃 기능
- endpoint: `POST /user/logout HTTP/1.1`


### Board

1. 게시판 추가 기능

2. 게시판 목록 조회 기능

3. 게시판 이름 변경 기능

4. 게시판 제거 기능

5.


### Article

## How to Run
