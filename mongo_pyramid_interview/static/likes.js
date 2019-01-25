function getSpan(linkElement) {
  return linkElement.querySelector('span')
}

function getAllSpans(videoItem) {
  let result = {}
  videoItem.querySelectorAll('span').forEach(element => {
    switch (element.className) {
      case 'theme':
      case 'likes':
      case 'dislikes':
        result[element.className] = element
    }
  })

  return result
}

function setValue(spanElement, value) {
  spanElement.textContent = value
}

function incrementValue(spanElement) {
  oldValue = parseInt(spanElement.textContent, 10)
  spanElement.textContent = oldValue + 1
}

function decrementValue(spanElement) {
  oldValue = parseInt(spanElement.textContent, 10)
  spanElement.textContent = Math.max(oldValue - 1, 0)
}

function likeVideo(event, video) {
  const spanElement = getSpan(event)
  incrementValue(spanElement)
  setTimeout(() => {
    fetch('/like_video', {
      method: 'post',
      body: JSON.stringify({ name: video }), 
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(function (response) {
      return response.json()
    }).then(function (data) {
      const spans = getAllSpans(event.parentElement)
      setValue(spans.likes, data.likes + "")
      setValue(spans.dislikes, data.dislikes + "")
      setValue(spans.theme, data.theme)
    }).catch(
      decrementValue(spanElement)
    )
  }, 0);
}

function dislikeVideo(event, video) {
  const spanElement = getSpan(event)
  incrementValue(spanElement)
  setTimeout(() => {
    fetch('/dislike_video', {
      method: 'post',
      body: JSON.stringify({ name: video }),
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(function (response) {
      return response.json()
    }).then(function (data) {
      const spans = getAllSpans(event.parentElement)
      setValue(spans.likes, data.likes + "")
      setValue(spans.dislikes, data.dislikes + "")
      setValue(spans.theme, data.theme)
    }).catch(
      decrementValue(spanElement)
    )
  }, 0);
}