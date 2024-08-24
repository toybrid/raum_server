# Technology Stack
```mermaid
    flowchart TD
        subgraph Docker Container
            Whitenoise --> Django
            Gunicorn --> Django
            Django-Ninja -->Django
        end
        subgraph Database AWS / Azure
            Django --> Postgres
        end
        subgraph Cloud Storage
            Django --> S3-storage
        end

        subgraph client
            Request -- Port: 8000 --> Django-Ninja
        end
```

# Database ORM

```mermaid
---
title: DB Design
---
classDiagram
    class User{
        + str email
        + str username
        + str first_name
        + str last_name
    }
    class RaumBaseClass{
        + datetime created_at
        + datetime modified_at
        + FK created_by
        + FK modified_by
        + bool active
    }
    class Project{
        + str code
        + str label
        + str client_name
    }
    class Container{
        + project
        + str code
        + str client_name
        + FK container_type
        + dict frame_range
    }
    class Product{
        + FK container
        + FK step
        + FK element
        + FK data_type
        + str lod
        + str layer
        + str task
        + str filepath
        + str extension
        + FK status
        + dict frame_range
        + int version
        + str slug
        + dict metadata
        + datetime approved_at
        + FK approved_by
        + save()
    }
    class ContainerRelationship{
        + FK from_container
        + FK relation_type
        + MTM to_containers
    }
    class ProductDependency{
        + FK product
        + MTM denpendencies
    }
    class Status{
        + str code
        + str label
    }
    class Step{
        + str code
        + str label
    }
    class Element{
        + str code
        + str label
    }
    class DataType{
        + str code
        + str label
    }
    class RelationType{
        + str code
        + str label
    }
    class ContainerType{
        + str code
        + str label
    }
    Project --> Container
    Container --> Product
    Container --> ContainerRelationship
    ContainerType --> Container
    Status --> Product
    Step --> Product
    DataType --> Product
    Element --> Product
    RelationType --> ContainerRelationship
    Product --> ProductDependency
    User --> RaumBaseClass
```