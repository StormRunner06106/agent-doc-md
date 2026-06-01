---
agent_doc_session: null
agent: codex
agent_doc_format: template
agent_doc_write: crdt
links:
- https://react.dev/learn/installation
- https://react.dev/learn/build-a-react-app-from-scratch
- https://vite.dev/guide/
---

# Session: Create a React Application

## User

## Status

<!-- agent:status patch=replace -->
<!-- /agent:status -->

## Exchange

<!-- agent:exchange patch=append -->
#User
How do I create a React application?

### Re: Create a React Application — gpt-5

The modern beginner-friendly way to create a plain React application is to use Vite.

#### Prerequisites

- Install Node.js.
- Use a terminal from the folder where you want the project to live.
- Create React App is deprecated for new React applications, so prefer Vite or a React framework.

#### Create the app

```bash
npm create vite@latest my-react-app -- --template react
cd my-react-app
npm install
npm run dev
```

After running `npm run dev`, Vite will print a local URL such as:

```text
http://localhost:5173/
```

Open that URL in your browser to see the React app.

#### Common project commands

```bash
npm run dev
```

Starts the development server.

```bash
npm run build
```

Creates a production build.

```bash
npm run preview
```

Previews the production build locally.

#### Main files to edit

- `src/App.jsx`: the main React component.
- `src/main.jsx`: the app entry point.
- `src/App.css`: styles for the starter app.
- `package.json`: project scripts and dependencies.

#### Optional TypeScript version

Use this command if you want React with TypeScript:

```bash
npm create vite@latest my-react-app -- --template react-ts
```

<!-- agent:boundary:create-react-app-guide -->
<!-- /agent:exchange -->

## Queue

<!-- agent:queue -->
<!-- /agent:queue -->

## Backlog

<!-- agent:backlog -->
<!-- /agent:backlog -->

## Icebox

<!-- agent:icebox -->
<!-- /agent:icebox -->
