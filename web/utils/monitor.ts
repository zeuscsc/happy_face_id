import express from 'express'
import { cyan, reset } from 'asciichart'
import { logger } from './logger'

export function monitorRequest(req : express.Request, res : express.Response, next:express.NextFunction)  {
    let date = new Date()
    let y = date.getFullYear()
    let m = d2(date.getMonth() + 1)
    let d = d2(date.getDate())
    let H = d2(date.getHours())
    let M = d2(date.getMinutes())
    let S = d2(date.getSeconds())
    let counter = req.session['counter']
    logger.info(
      `[${cyan}${y}-${m}-${d} ${H}:${M}:${S}${reset}] (${counter}) ${req.method} ${req.url}`,
    )
    next()
  }

  function d2(x: number): string {
    if (x < 10) {
      return '0' + x
    }
    return String(x)
  }


  export function counter(req : express.Request, res : express.Response, next:express.NextFunction) {
    let counter = req.session['counter'] || 0
    counter++
    req.session['counter'] = counter
  
    // this is optional, it should auto save
    // But for realtime update in concurrent requests, better call the save method explicitly
    req.session.save()
    next()
  }