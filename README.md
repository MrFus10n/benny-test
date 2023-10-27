# This is a test task project
## How to start
1. Clone the project.
2. Extract `env.zip` file. There is an `.env` file with secrets.
3. Run `docker-compose up`
4. Visit http://localhost:8000/
5. To run tests, run `docker-compose run --rm backend python manage.py test`

## Bonus features
1. Hot module replacement.
2. REST API.
3. Fully typed API client is generated and front is compiled automatically once a change in backend code is saved.
4. Working autocomplete for the API on front.
5. Front does not compile when API calls are broken.
6. React is served by backend to be as close as possible to production environment setup.
7. Material UI.

## Notes about the tasks
### OAUTH
On the backend it's implemented using `allauth`. On the frontend, see 
`frontend/src/components/LoginButton/LoginButton.tsx` file. 
The button submits `allauth` login form, all the rest is done under the hood.

The form logic and button layout are encapsulated, for ease of adding more of them.

### Parsing
See `backend/core/parser.py` The main method is `Parser.parse`. 
`spaCy` is used for NLP where needed. The logic of parsing is next:
1. Split the input into paragraphs.
2. Find the paragraph which is most likely responsible for period by looking for the amount related keywords and dates.
3. Within that paragraph, find all dates without year, as we are not interested in absolute dates.
4. Make consecutive start-end periods from the dates found. If distance between 2 consecutive dates is more than 1 day it is considered a period.
5. Find the paragraph which is most likely responsible for contribution amounts by looking for the amount related keywords and dates.
6. Find all the % and $ amounts.
7. If there is only one value in a group, it's considered maximum (there is no reason to provide only minimum contribution amount).
8. If there are values in both groups, then the output is `x% or $y`.

## Request processing
1. Browser sends request to the `backend` service.
2. `backend` service looks for `webpack-stats.json` file in the `frontend/build` directory.
3. `backend` service reads the bundle file address from `webpack-stats.json`.
4. `backend` service renders the page with the bundle.

## API client sync flow
1. Developer changes its files of the `backend` service, which triggers its reload.
2. `backend` service generates `backend/conf/openapi_schema.json` file with `openapi` schema.
3. `api-client-builder` service detects the change in the file and runs API client generation.
4. API client generation modifies files in `frontend/src/api` directory, which triggers frontend recompile.
5. On recompile, web page reloads.
