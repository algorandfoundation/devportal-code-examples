export const getOperationMessage = (operation: 'create' | 'update' | 'replace' | 'nothing') => {
  switch (operation) {
    case 'create':
      return '🎉  New application deployed successfully!'
    case 'update':
      return '✨  Application updated successfully!'
    case 'replace':
      return '🔄  Application replaced successfully!'
    case 'nothing':
      return 'ℹ️  No changes needed - application is up to date'
  }
}
