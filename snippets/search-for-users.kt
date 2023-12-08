// The following snippet is a user-finding algorithm derived from a Android social media app.

fun searchForUsers(
  query: String,
  fresh: Boolean,
  queryLimit: Int,
  callBack: (() -> Unit)? = null,
) {

  lastQuery = query
  if (fresh) {
    tmpValue = 0
    aggScroll = 0
    aggScrollThreshold = 0
    queryPos = 0
    queryUpperRange = 0
    viewCount = 0
    iMap.clear()
  }

  val activity = requireActivity() as LandingActivity
  val username = activity.username
  val token = activity.token
  val handler = Handler(requireContext().mainLooper)
  val logTag = "SearchPeople"

  val removeViews = fun() {
    binding.linearLayout.removeAllViews()
    binding.scrollView.scrollTo(0, 0)
    viewCount = 0
  }

  Executors.newSingleThreadExecutor().execute {

    try {

      val bufferS = if (query == "") {
        "search-for-users&$token&$username&$queryPos&$queryLimit;"
      } else {
        "search-for-users-query&$token&$username&$queryPos&$queryLimit&$query;"
      }

      queryUpperRange = queryPos + (queryLimit - 1)

      Log.d(
        logTag,
        "queryRange: $queryPos->$queryUpperRange (fresh=$fresh)," +
                " viewCount: $viewCount, ratio=${
                  (queryUpperRange * 1.0f) / (Math.max(
                    viewCount,
                    1
                  ) * 1.0f)
                }"
      )

      activity.restorePeopleQuery = query
      activity.restorePeopleQueryP = true

      queryPos += queryLimit // Fine to go here, even if we end up with extra data
      activity.restorePeopleQueryLimit = queryPos

      Log.d(
        logTag, "username=$username, token=$token, query=$query, lQ=$lastQuery qL=$queryLimit, " +
                "queryPos=$queryPos"
      )

      requestData(bufferS, fun(line: String) {

        //Log.d(logTag, "Got line: '$line'")
        if (isSuccess(line)) {

          var users = line.split(";")

          // Handle trailing ;
          if (users[users.size - 1] == "")
            users = users.subList(0, users.size - 1)

          Log.d(logTag, "Successfully searched for users as $username: Got $line")
          Log.d(logTag, "Got ${users.size} users")

          handler.post {

            if (_binding == null)
              return@post

            if (fresh)
              removeViews()

            var i = 0
            val views = ArrayList<View>()
            var glideElapsedMS: Long = 0
            val elapsedMS = measureTimeMillis {
              for (user in users) {
                if (user == "")
                  continue
                val split = user.split(":")
                // age (name)
                val name = split[2] + " (" + split[1] + ")"
                val distance = split[3]
                val avatar = URLDecoder.decode(split[5], "UTF-8")
                val uID = split[0]
                  Log.d(logTag, "Found user: $split")
                //Log.d(logTag, "Found image: $avatar")
                  if (i == 0)
                    Log.d(logTag, "Adding views for user")
                val button = CircleImageView(context) // like 'ImageButton(context)'
                button.minimumWidth = 211
                button.minimumHeight = 211
                button.setOnClickListener {
                  button.colorFilter = PorterDuffColorFilter(
                    Color.parseColor("#66f900ff"),
                    PorterDuff.Mode.ADD
                  )
                  Executors.newSingleThreadExecutor().execute {
                    for (j in 1..40) {
                      Thread.sleep(15)
                      var opacity = Integer.toHexString((40 - j) * (255 / 100))
                      //Log.d("j", "$j, $opacity, ${(40-j)*(255/100)}")
                      if (opacity.length == 1)
                        opacity = "0$opacity"
                      button.colorFilter = PorterDuffColorFilter(
                        Color.parseColor("#" + opacity + "f900ff"),
                        PorterDuff.Mode.ADD
                      )
                    }
                    button.colorFilter = null
                  }
                  @Suppress("NAME_SHADOWING")
                  Executors.newSingleThreadExecutor().execute {
                    requestData("request-user&$token&$username&$uID;", fun(line: String) {
                      val logTag = "SearchPeople (callback)"
                      if (isSuccess(line)) {
                        //Log.d(logTag, "Successfully requested user: Got '$line'")
                        var parts = line.split("&")
                        if (line.startsWith("chat")) {
                          parts = parts.subList(1, parts.size)
                          val otherUser = parts[0]
                          val otherName = parts[1]
                          val chatStack = parts[2]
                          val chatStackTip = parts[3]
                            Log.d(
                              logTag,
                              "Callback: Already friends with $otherUser ($otherName): Entering chat."
                            )
                          handler.post {
                            showChat(otherUser, otherName, chatStack, chatStackTip)
                          }
                        } else {
                          if (line != "success")
                            Log.d(logTag, "Invalid data format: '$line'")
                        }
                      } else {
                        Log.e(logTag, "An error occurred in the callback: Server says: $line")
                      }
                    })
                  }
                }

                // NOTE color on the default avatar is #88badc or so
                // Remove background, keep animation (unlike button.setBackgroundColor)
                //button.backgroundTintMode = PorterDuff.Mode.ADD
                val text = TextView(context)
                iMap[uID] = iMap.size + 1
                text.text = name// + if (debugMode) " (DEBUG: ${iMap[uID]})" else ""

                val dist = TextView(context)
                dist.text = distance

                val params = LinearLayout.LayoutParams(
                  LinearLayout.LayoutParams.WRAP_CONTENT,
                  LinearLayout.LayoutParams.WRAP_CONTENT
                )

                val params2 = LinearLayout.LayoutParams(
                  LinearLayout.LayoutParams.WRAP_CONTENT,
                  LinearLayout.LayoutParams.WRAP_CONTENT
                )

                params.setMargins(15, 60, 0, 0)
                params2.setMargins(15, 0, 0, 0)
                i++

                glideElapsedMS += measureNanoTime {
                  Glide.with(this@PeopleFragment)
                    .load(avatar)
                    .apply(RequestOptions().override(211, 211))
                    .into(button)
                }

                binding.linearLayout.addView(button, params)
                binding.linearLayout.addView(text, params2)
                binding.linearLayout.addView(dist, params2)
                views.add(button)
                views.add(text)
                views.add(dist)
                viewCount++
              }
            }

            glideElapsedMS /= 1000
            glideElapsedMS /= 1000
              Log.d(
                logTag,
                "elapsedMS(inner)=$elapsedMS, glideElapsedMS(inner)=$glideElapsedMS for users=[${users.size}]"
              )
              // Log.d(logTag, "views=[${views.size}]")
              Log.d(logTag, "elapsedMS(outer)=${System.currentTimeMillis()-ms1} for users=[${users.size}]")
            if (callBack != null) {
              handler.post {
                callBack()
              }
            }
          }
        } else {
          if (fresh) {
            Log.e(logTag, "Failed to search for users: Server says: $line")
              Log.d(logTag, "elapsedMS(outer)=${System.currentTimeMillis() - ms1} for users=???")
            if (line == "ERROR: No matching users were found.") {
              val text = TextView(context)
              text.text = "Unfortunately, we couldn't find anyone who lives near you."
              val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
              )
              params.setMargins(15, 60, 0, 0)
              handler.post {
                removeViews()
                binding.linearLayout.addView(text, params)
              }
            } else
              throw Exception("Failed to search for users: $line")
          }
        }
      })
    } catch (e: Throwable) {
        Log.d(logTag, "elapsedMS(outer)=${System.currentTimeMillis()-ms1} for users=???")
      Log.e("Error logging in", e.toString())
      throw IOException("Error logging in (no data)", e)
    }
  }
}