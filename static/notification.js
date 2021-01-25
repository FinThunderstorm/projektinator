const hideNotification = () => {
  window.document.getElementsByName('notification')[0].hidden = true
}
window.onload = () => {
  // wanted seconds * 1000 milliseconds = seconds
  showTime = 10 * 1000
  setTimeout(hideNotification, showTime)
}