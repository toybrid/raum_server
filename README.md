# Raum

Raum is a streamlined asset management system tailored for use in 3D animation and VFX production studios, exclusively focused on versioning assets and meticulously tracing their dependencies. It is important to note that Raum is primarily designed for asset management, not for production tracking.

## Technology stack

Raum is constructed using Django 4.2 as its foundation, with PostgreSQL serving as the backend database.

## Design

Raum features an uncomplicated design comprising only three primary tables: Bundle, Product, and Dependency. The core objective of Raum is to generate distinctive version stacks based on specified properties and meticulously monitor file dependencies.

Raum also has a simple OOP based client api.

Raum's abstract design will work well with existing production tracking softwares like shotgrid or ftrack and the api will allow to communicate between each other very easily

Raum's http url can be used along with custom USD Asset Resolver also easily

## Enviroment Variables
| Variable    | Description |
| -------- | ------- |
| RAUM_SECRECT_KEY  | Secret key for django application    
| RAUM_SETTINGS_MODULE | Custom settings module     |
| RAUM_DEBUG    | Enable debug features don't use in prod  |
| RAUM_DEV_DB_NAME    | Name of development databse    |
| RAUM_DEV_DB_USER    | Development database user    |
| RAUM_DEV_DB_PORT    | Development database server port    |
| RAUM_DEV_DB_PASSWORD    | Development database server password    |
| RAUM_DEV_DB_HOST    | Development database Host name    |
| RAUM_PAGINATION_SIZE    | Default pagination size    |
| RAUM_TOKEN_TIMEOUT    | Expiry for authentication token   |
| RAUM_ALLOWED_EMAIL_DOMAINS    | Allowed email domains for registry comma separated   |
| RAUM_ALLOWED_HOSTS    | Allowd host list comma separated    |

## Upcoming
* Thumbnails for products
* Archive project
* MFD extension service
* Project based access control
* Public docker image
* Docker compose

## Deployment