# start development server
npm run dev

# Save dependencies to txt file:
npm list --prod --depth=0 > requirements.txt

(npm list --omit=dev --depth=0 | Out-String) | Set-Content requirements.txt