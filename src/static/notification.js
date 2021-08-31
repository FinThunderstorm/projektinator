const hideNotification = () => {
  notificationBox = window.document.getElementsByName('notification')[0]
  if(notificationBox){
    notificationBox.hidden = true
  }
}
window.onload = () => {
  // wanted seconds * 1000 milliseconds = seconds
  showTime = 10 * 1000
  setTimeout(hideNotification, showTime)
}