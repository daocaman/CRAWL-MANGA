module.exports = {
  // TypeScript and JavaScript files
  '**/*.{js,jsx,ts,tsx}': [
    // Run ESLint with auto-fix
    (filenames) => `eslint ${filenames.join(' ')} --fix`,

    // Run Prettier to format
    (filenames) => `prettier --write ${filenames.join(' ')}`,

    // Add changed files back to git staging
    'git add',
  ],

  // CSS and Style files
  '**/*.{css,scss,less}': [
    // Format style files
    (filenames) => `prettier --write ${filenames.join(' ')}`,
    'git add',
  ],

  // Markdown and JSON files
  '**/*.{md,json}': [
    // Format markdown and JSON
    (filenames) => `prettier --write ${filenames.join(' ')}`,
    'git add',
  ],

  // HTML files
  '**/*.html': [
    // Format HTML
    (filenames) => `prettier --write ${filenames.join(' ')}`,
    'git add',
  ],
};
