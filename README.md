# Raum

Raum is a streamlined asset management system tailored for use in 3D animation and VFX production studios, exclusively focused on versioning assets and meticulously tracing their dependencies. It is important to note that Raum is primarily designed for asset management, not for production tracking.

## Technology stack

Raum is constructed using Django 4.2 as its foundation, with PostgreSQL serving as the backend database.

## Design

Raum features an uncomplicated design comprising only three primary tables: Bundle, Product, and Dependency. The core objective of Raum is to generate distinctive version stacks based on specified properties and meticulously monitor file dependencies.

Raum also has a simple OOP based client api.

Raum's abstract design will work well with existing production tracking softwares like shotgrid or ftrack and the api will allow to communicate between each other very easily

Raum's http url can be used along with custom USD Asset Resolver also easily

## Upcoming
* Thumbnails for products
* Archive project
* MFD extension service