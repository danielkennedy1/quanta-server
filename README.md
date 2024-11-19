# QUANTA SERVER

## Description
This repository contains the backend of the Quanta project.

## Technologies
- Connexion
- Flask
- SQLAlchemy
- Generated python code from OpenAPI specification

## Design Considerations
- Hexagonal architecture (ports and adapters) - Domain never depends on adapters, both depend on configuration
- RESTful API
- OpenAPI specification
- Repository pattern
- Dependency injection for services and concrete repositories

## TODO
- [ ] Add tests
- [ ] Add timestamp to responses

