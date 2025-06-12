# Djmode CLI Commands

## Project Initialization
- `pdm init`

- `pdm install`

- `djmode init`  
  Initialize a new Djmode-based Django project.

- `djmode install`  
  Install all dependencies and prepare the environment.

---

## Module Management
- `djmode create module -n <module_name> -v <version> -f <field>:<type>:<options> ...`  
  Create a new module with fields (similar to `rails generate model`).

- `djmode update module -n <module_name> -v <version> -f <field>:<type>:<options> ...`  
  Update or add new fields to an existing module.

- `djmode remove module -n <module_name> -v <version>`  
  Remove a specific module and its components.

- `djmode list modules`  
  List all created modules.

---

## Module Actions
- `djmode add module actions -n <module_name> -v <version> --actions <action1> <action2> ...`  
  Add standard or custom actions to a module (e.g., `create_one`, `find_all`).

- `djmode remove module actions -n <module_name> -v <version> --actions <action1> <action2> ...`  
  Remove specific actions from a module.

---

## Module Views
- `djmode create module views -n <module_name> -v <version>`  
  Generate default views for list, detail, create, update, delete.

- `djmode remove module views -n <module_name> -v <version>`  
  Remove generated views.

---

## Routing & Endpoints
- `djmode show module routes -n <module_name> -v <version>`  
  Show generated API routes for the module (similar to `rails routes`).

---

## Database & Seeds
- `djmode makemigrations -n <module_name> -v <version>`  
  Create database migration files (similar to `rails generate migration`).

- `djmode migrate -n <module_name> -v <version>`  
  Apply pending migrations to the database.

- `djmode runseed -n <module_name> -v <version>`  
  Populate the database with seed data for development/testing.

---

## Module Inspection
- `djmode show module model -n <module_name> -v <version>`  
  Display the model definition for the module.

- `djmode show module actions -n <module_name> -v <version>`  
  List all actions available for the module.

- `djmode show module services -n <module_name> -v <version>`  
  Show service layer functions (business logic).

- `djmode show module repositories -n <module_name> -v <version>`  
  Show data access and query logic.

- `djmode show module schema -n <module_name> -v <version>`  
  Display complete schema of the module.

- `djmode show module history -n <module_name> -v <version>`  
  Display creation and modification history.

---

## Project Utilities
- `djmode show project tree`  
  Visualize the full structure of the project (like `rails stats` + `tree`).

- `djmode show project history`  
  Display history of all module operations across the project.

- `djmode console`  
  Start an interactive shell with project context (like `rails console`).

- `djmode server`  
  Run the development server (wrapper for `python manage.py runserver`).

---

## Testing
- `djmode test -n <module_name> -v <version>`  
  Run tests scoped to a specific module and version.

- `djmode test all`  
  Run the entire test suite for the project.

---

## Shortcuts Inspired by Rails
- `djmode generate scaffold -n <module_name> -v <version> -f <field>:<type>:<options>`  
  Generate model, views, actions, routes, and migrations all at once.

- `djmode destroy module -n <module_name> -v <version>`  
  Fully remove a module (model, views, actions, routes, migrations).
