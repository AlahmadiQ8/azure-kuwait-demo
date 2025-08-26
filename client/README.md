# Kuwait Fine Dining - Frontend

This is the frontend application for Kuwait Fine Dining, built with Astro and Svelte. The frontend provides an elegant, dark-themed interface for discovering restaurants in Kuwait.

## 🚀 Technology Stack

- **Astro** - Static site generator and page routing
- **Svelte** - Interactive components with reactive programming
- **Tailwind CSS v4** - Utility-first CSS with modern dark theme
- **TypeScript** - Type-safe JavaScript
- **Playwright** - End-to-end testing

## 🏗️ Project Structure

```
client/
├── src/
│   ├── components/        # Reusable Svelte components
│   │   ├── RestaurantList.svelte
│   │   └── RestaurantDetails.svelte
│   ├── layouts/          # Astro layout templates
│   │   └── Layout.astro
│   ├── pages/            # Astro page routes
│   │   ├── index.astro
│   │   └── about.astro
│   └── styles/           # Global styles and Tailwind config
├── e2e-tests/           # Playwright end-to-end tests
├── public/              # Static assets
└── dist/               # Built files (generated)
```

## 🧞 Commands

All commands should be run from the client directory:

| Command | Action |
| :------ | :----- |
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server at `localhost:4321` |
| `npm run build` | Build production site to `./dist/` |
| `npm run preview` | Preview production build locally |
| `npm run test:e2e` | Run Playwright end-to-end tests |
| `npm run astro ...` | Run Astro CLI commands |
| `npm run astro -- --help` | Get help with Astro CLI |

## 🎨 Styling Guidelines

- **Dark Mode**: All components use a dark theme with slate colors
- **Tailwind CSS**: Use utility classes for styling
- **Rounded Corners**: Apply rounded corners to UI elements for modern look
- **Responsive**: Design should work on mobile, tablet, and desktop
- **Accessibility**: Follow WCAG guidelines for accessible interfaces

## 🔧 Development

### Starting Development Server
```bash
npm run dev
```
The site will be available at `http://localhost:4321`

### Building for Production
```bash
npm run build
npm run preview  # Preview the build
```

### Running Tests
```bash
npm run test:e2e
```

## 📱 Pages

- **Home** (`/`) - Restaurant listings and search
- **About** (`/about`) - Information about the platform
- **Restaurant Details** (`/restaurant/[id]`) - Individual restaurant pages

## 🌐 API Integration

The frontend connects to the Flask backend API running on `http://localhost:5100`. API integration is handled through:

- Fetch requests in Svelte components
- Server-side rendering in Astro pages where appropriate
- Type-safe API calls with TypeScript

## 🧪 Testing

End-to-end tests are written with Playwright and cover:
- Page loading and navigation
- Restaurant listing functionality
- Search and filtering features
- Mobile responsiveness

## 🚀 Deployment

The application is built as a server-side rendered (SSR) site using the Node.js adapter. For deployment:

1. Run `npm run build`
2. Deploy the `dist/` folder to your hosting platform
3. Ensure the backend API is accessible from your production environment

---

For more information about the full project setup, see the main [README.md](../README.md) in the project root.
