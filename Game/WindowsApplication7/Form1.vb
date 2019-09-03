
Public Class Form1
    Dim rightbutton, newframe, picturewidth, pictureheigth, leftbutton, upbutton, downbutton, nowshooting, bulletcount, timewhenshooting, frames, aimx, aimy, mousey, mousex, t As Integer
    Dim picture As Bitmap
    Dim hero As human
    Dim crazydistance As Integer = 225
    Dim crazyspeedmultiplier As Integer = 2.75
    Dim bulletspeed As Integer = 8
    Dim enemiescount As Integer = 0
    Dim enemyspeed As Integer = 2
    Dim enemy(1) As alien
    Dim enemyhp As Integer = 3
    Dim bulletsquantity As Integer = 50
    Dim bullet(bulletsquantity) As bullets
    Declare Sub GetCursorPos Lib "User" (ByVal lpPoint As pointapi)
    Dim cursorpos As pointapi
    Dim enemyanimate(enemiescount) As Integer
    Dim herohp As Integer = 5
    Dim frametime As Integer = 10
    Dim coeff As Double
    Dim timetodissappear As Integer = 10000
    Dim starttime As Integer
    Dim enemieskilled As Integer
    Dim bulletsfired As Integer
    Dim bulletsachievedenemy As Integer
    Dim guntemperature As Integer
    Dim prevcooltime As Integer
    Dim paused As Integer = -1
    Dim gamestopped As Integer
    Dim prevspawntime As Integer
    Dim pen1 As New System.Drawing.Pen(Color.Purple, 2)

    Private Sub unfocused(sender As Object, e As EventArgs) Handles Me.Deactivate
        paused = 1
    End Sub
    Private Sub Form1_FormClosed(sender As Object, e As FormClosedEventArgs) Handles Me.FormClosed
        gamestopped = 1
    End Sub
    Structure pointapi
        Dim x As Integer
        Dim y As Integer
    End Structure
    Structure human
        Dim width, height, x, y, speed, hp, orientation, xspeed, yspeed As Integer '1 вверх,  2 вниз, 3 влево, 4 вправо
        Dim angle As Double
    End Structure
    Structure bullets
        Dim x, y, xspeed, yspeed, size, active, damage, width, height As Integer
    End Structure
    Structure alien
        Dim x, y, aimx, aimy, hp, active, width, height, framesleft, timetodissappear, alive, type As Integer
        Dim xspeed, yspeed, angle As Double
        Dim angledcoord(,) As Point 'координаты точек с учетом поворота врага
        Dim drawingcoor, ds As Point()
    End Structure
    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load

        hero.height = My.Resources.hero.Height
        hero.width = My.Resources.hero.Width
        hero.x = Me.Width / 2 - hero.width
        hero.y = Me.Height / 2 - hero.width
        hero.speed = 4
        hero.hp = herohp
        For i = 0 To enemiescount
            enemy(i).aimy = hero.y + 0.5 * hero.height
            enemy(i).aimx = hero.x + 0.5 * hero.width
        Next
    End Sub
    Sub gameover()
        ProgressBar1.Value = hero.hp
        gamestopped = 1
        MsgBox("Врагов убито: " & enemieskilled & "." & Chr(10) & "Выпущено " & bulletsfired & " снарядов, из них " & bulletsachievedenemy & " попало в цель.")
        Application.Exit()
    End Sub
    Sub bulletsappear()
        If nowshooting = 1 And Environment.TickCount > timewhenshooting + 350 And guntemperature <= 190 Then
            guntemperature += 10
            bulletsfired += 1
            timewhenshooting = Environment.TickCount
            If bulletcount < bulletsquantity Then
                bulletcount += 1
            Else
                bulletcount = 1
            End If
            bullet(bulletcount).active = 1
            bullet(bulletcount).damage = 1
            bullet(bulletcount).width = My.Resources.bullet.Width
            bullet(bulletcount).height = My.Resources.bullet.Height
            bullet(bulletcount).x = hero.x + hero.width * 0.5
            bullet(bulletcount).y = hero.y + hero.height * 0.5
            frames = Math.Sqrt((mousex - hero.x - hero.width * 0.5) ^ 2 + (mousey - hero.y - hero.height * 0.5) ^ 2) / bulletspeed
            bullet(bulletcount).xspeed = (mousex - hero.x - hero.width * 0.5) / frames
            bullet(bulletcount).yspeed = (mousey - hero.y - hero.height * 0.5) / frames
            coeff = Math.Sqrt(bullet(bulletcount).xspeed ^ 2 + bullet(bulletcount).yspeed ^ 2) / bulletspeed
            bullet(bulletcount).xspeed = bullet(bulletcount).xspeed / coeff
            bullet(bulletcount).yspeed = bullet(bulletcount).yspeed / coeff
            My.Computer.Audio.Play(My.Resources.shot, AudioPlayMode.Background)
        End If
    End Sub
    Sub bulletsmove()
        For i = 1 To bulletsquantity
            If bullet(i).x + bullet(i).xspeed > 1 And bullet(i).x + bullet(i).xspeed + bullet(i).width < PictureBox1.Width Then
                bullet(i).x += bullet(i).xspeed
            Else
                bullet(i).xspeed = 0
                bullet(i).yspeed = 0
                bullet(i).active = 0
            End If
            If bullet(i).y + bullet(i).yspeed > 1 And bullet(i).y + bullet(i).yspeed + bullet(i).height < PictureBox1.Height Then
                bullet(i).y += bullet(i).yspeed
            Else
                bullet(i).xspeed = 0
                bullet(i).yspeed = 0
                bullet(i).active = 0
            End If
        Next
    End Sub
    Sub enemyappears()
        enemiescount += 1
        ReDim Preserve enemy(enemiescount)
        ReDim enemy(enemiescount).angledcoord(1, 1)
        enemy(enemiescount).framesleft = 0
        enemy(enemiescount).hp = enemyhp
        enemy(enemiescount).active = 1
        enemy(enemiescount).width = My.Resources.enemy.Width
        enemy(enemiescount).height = My.Resources.enemy.Height
        enemy(enemiescount).hp = enemyhp
        enemy(enemiescount).alive = 1
        Dim z As Integer
        Randomize()
        z = Rnd() * 2 * Math.PI
        enemy(enemiescount).type = Rnd() * 2 - 1
        enemy(enemiescount).x = Math.Cos(z) * Me.Width
        enemy(enemiescount).y = Math.Sin(z) * Me.Width
    End Sub
    Sub enemiesmove()
        For i = 1 To enemiescount
            If enemy(i).alive = 1 Then
                If (hero.x - enemy(i).x) ^ 2 + (hero.y - enemy(i).y) ^ 2 > crazydistance ^ 2 And enemy(i).type = 0 Then
                    Dim angle, aimangle As Double
                    angle = Math.Atan((enemy(i).y - hero.y) / (hero.x - enemy(i).x))
                    If hero.x - enemy(i).x < 0 Then
                        angle += Math.PI
                    End If
                    aimx = Rnd() * Me.Width / 10
                    aimy = ((Rnd() - 0.5) * 2) * Me.Width / 5
                    aimangle = Math.Atan(aimy / aimx)
                    enemy(i).yspeed = enemyspeed * Math.Sin(aimangle - angle)
                    enemy(i).xspeed = enemyspeed * Math.Cos(aimangle - angle)
                    enemy(i).framesleft = Math.Sqrt(aimx ^ 2 + aimy ^ 2) / enemyspeed
                ElseIf (hero.x - enemy(i).x) ^ 2 + (hero.y - enemy(i).y) ^ 2 < crazydistance ^ 2 And enemy(i).type = 0 Then
                    enemy(i).framesleft = Math.Sqrt((hero.x - enemy(i).x) ^ 2 + (hero.y - enemy(i).y) ^ 2) / enemyspeed / crazyspeedmultiplier
                    If enemy(i).framesleft = 0 Then enemy(i).framesleft = 1
                    enemy(i).xspeed = (hero.x - enemy(i).x) / enemy(i).framesleft
                    enemy(i).yspeed = (hero.y - enemy(i).y) / enemy(i).framesleft
                ElseIf enemy(i).type = 1 Then
                    enemy(i).framesleft = Math.Sqrt((hero.x - enemy(i).x) ^ 2 + (hero.y - enemy(i).y) ^ 2) / enemyspeed / crazyspeedmultiplier
                    If enemy(i).framesleft = 0 Then enemy(i).framesleft = 1
                    enemy(i).xspeed = (hero.x - enemy(i).x) / enemy(i).framesleft
                    enemy(i).yspeed = (hero.y - enemy(i).y) / enemy(i).framesleft
                End If
            End If
            If enemy(i).alive = 1 Then
                enemy(i).angle = Math.Sign(hero.y - enemy(i).y - 0.5 * enemy(i).height) * Math.Acos((hero.x - enemy(i).x - 0.5 * enemy(i).width) / Math.Sqrt((hero.x - enemy(i).x - 0.5 * enemy(i).width) ^ 2 + (hero.y - enemy(i).y - 0.5 * enemy(i).height) ^ 2))
            End If
            Dim enemydiag As Double = 0.5 * Math.Sqrt(enemy(i).height ^ 2 + enemy(i).width ^ 2)
            If enemy(i).width = 0 Then
                enemy(i).xspeed = enemy(i).xspeed
            End If
            Dim defaultangle As Double = Math.Atan(enemy(i).height / enemy(i).width)
            enemy(i).angledcoord(0, 1).X = Math.Cos(Math.PI - defaultangle + enemy(i).angle) * enemydiag + 0.5 * enemy(i).width
            enemy(i).angledcoord(0, 1).Y = Math.Sin(Math.PI - defaultangle + enemy(i).angle) * enemydiag + 0.5 * enemy(i).height
            enemy(i).angledcoord(1, 1).X = Math.Cos(defaultangle + enemy(i).angle) * enemydiag + 0.5 * enemy(i).width
            enemy(i).angledcoord(1, 1).Y = Math.Sin(defaultangle + enemy(i).angle) * enemydiag + 0.5 * enemy(i).height
            enemy(i).angledcoord(1, 0).X = Math.Cos(-defaultangle + enemy(i).angle) * enemydiag + 0.5 * enemy(i).width
            enemy(i).angledcoord(1, 0).Y = Math.Sin(-defaultangle + enemy(i).angle) * enemydiag + 0.5 * enemy(i).height
            enemy(i).angledcoord(0, 0).X = Math.Cos(Math.PI + defaultangle + enemy(i).angle) * enemydiag + 0.5 * enemy(i).width
            enemy(i).angledcoord(0, 0).Y = Math.Sin(Math.PI + defaultangle + enemy(i).angle) * enemydiag + 0.5 * enemy(i).height
            'Dim enemy(i).drawngcoords As Point() = {enemy(i).angledcoord(0, 0), enemy(i).angledcoord(1, 0), enemy(i).angledcoord(0, 1)}
        Next

    End Sub
    Sub heromoves()
        If rightbutton = 1 And hero.x + hero.speed + hero.width < PictureBox1.Width Then hero.xspeed = hero.speed
        If leftbutton = 1 And hero.x - hero.speed >= 0 Then hero.xspeed = -hero.speed
        If upbutton = 1 And hero.y - hero.speed >= 0 Then hero.yspeed = -hero.speed
        If downbutton = 1 And hero.y + hero.speed + hero.width < PictureBox1.Height Then hero.yspeed = hero.speed
        hero.x += hero.xspeed
        hero.y += hero.yspeed
        hero.yspeed = 0
        hero.xspeed = 0
        hero.angle = Math.Sign(mousey - hero.y - 0.5 * hero.height) * Math.Acos((mousex - hero.x - 0.5 * hero.width) / Math.Sqrt((mousex - hero.x - 0.5 * hero.width) ^ 2 + (mousey - hero.y - 0.5 * hero.height) ^ 2))
    End Sub
    Sub checkfordamage()
        For i = 1 To bulletsquantity
            For a = 1 To enemiescount
                If bullet(i).active = 1 And enemy(a).alive = 1 And bullet(i).x + bullet(i).width > enemy(a).x And bullet(i).x < enemy(a).x + enemy(a).width And bullet(i).y + bullet(i).height > enemy(a).y And bullet(i).y < enemy(a).y + enemy(a).height Then
                    enemy(a).hp -= bullet(i).damage
                    bullet(i).active = 0
                    bulletsachievedenemy += 1
                End If
            Next
        Next
        For i = 1 To enemiescount
            If enemy(i).alive = 1 And enemy(i).x + enemy(i).width > hero.x And enemy(i).x < hero.x + hero.width And enemy(i).y + enemy(i).height > hero.y And enemy(i).y < hero.y + hero.height Then
                enemy(i).hp = 0
                If hero.hp - 1 > 0 Then
                    hero.hp -= 1
                Else
                    hero.hp = 0
                End If
                If guntemperature + 30 <= 200 Then
                    guntemperature += 30
                Else
                    guntemperature = 200
                End If
            End If
        Next
        For i = 1 To enemiescount
            If enemy(i).hp <= 0 And enemy(i).active = 1 And enemy(i).alive = 1 Then
                enemieskilled += 1
                enemy(i).alive = 0
                enemy(i).timetodissappear = Environment.TickCount + timetodissappear
                If guntemperature - 30 >= 0 Then
                    guntemperature -= 30
                Else
                    guntemperature = 0
                End If

            End If
        Next

    End Sub
    Sub timers()
        For i = 1 To enemiescount
            If enemy(i).timetodissappear <> 0 And enemy(i).timetodissappear < Environment.TickCount Then
                enemy(i).active = 0
            End If
        Next
        If Environment.TickCount - prevspawntime > 750 Then
            enemyappears()
            prevspawntime = Environment.TickCount
        End If
        If prevcooltime + 200 < Environment.TickCount Then
            prevcooltime = Environment.TickCount
            If guntemperature > 0 Then guntemperature -= 1
        End If
    End Sub
    Sub main()
        t = 0
        starttime = Environment.TickCount
        Do
            For i = 1 To 100
                Application.DoEvents()
            Next
            If t < Environment.TickCount And paused = -1 Then
                frame()
            End If
            If hero.hp = 0 Or gamestopped = 1 Then
                Exit Do
            End If
        Loop
        gameover()
    End Sub
    Sub frame()
        t = Environment.TickCount + frametime
        bulletsappear()
        bulletsmove()
        For i = 1 To enemiescount
            If enemy(i).alive = 1 Then
                If enemy(i).framesleft = 0 Then
                    enemiesmove()
                End If
                enemy(i).x += enemy(i).xspeed
                enemy(i).y += enemy(i).yspeed
                enemy(i).framesleft -= 1
            End If
        Next
        heromoves()
        ProgressBar1.Value = hero.hp
        ProgressBar2.Value = guntemperature
        PictureBox1.Invalidate()
        PictureBox1.Update()
        newframe = 1
        checkfordamage()
        Randomize()
        timers()
    End Sub
    Private Sub paintall(ByVal sender As System.Object, ByVal e As System.Windows.Forms.PaintEventArgs) Handles PictureBox1.Paint
        For i = 1 To enemiescount
            If enemy(i).active = 1 Then
                If enemy(i).alive = 0 And enemy(i).type = 0 Then
                    e.Graphics.TranslateTransform(enemy(i).x + 0.5 * enemy(i).width, enemy(i).y + 0.5 * enemy(i).height)
                    e.Graphics.RotateTransform(enemy(i).angle * 180 / Math.PI)
                    e.Graphics.DrawImage(My.Resources.deadenemy, Convert.ToInt32(-0.5 * enemy(i).width), Convert.ToInt32(-0.5 * enemy(i).height))
                    e.Graphics.RotateTransform(-enemy(i).angle * 180 / Math.PI)
                    e.Graphics.TranslateTransform(-enemy(i).x - 0.5 * enemy(i).width, -enemy(i).y - 0.5 * enemy(i).height)
                    'e.Graphics.DrawImage(My.Resources.deadenemy, enemy(i).drawingcoords)
                ElseIf enemy(i).hp = 1 And enemy(i).alive = 1 And enemy(i).type = 0 Then
                    e.Graphics.TranslateTransform(enemy(i).x + 0.5 * enemy(i).width, enemy(i).y + 0.5 * enemy(i).height)
                    e.Graphics.RotateTransform(enemy(i).angle * 180 / Math.PI)
                    e.Graphics.DrawImage(My.Resources.heavydamagedenemy, Convert.ToInt32(-0.5 * enemy(i).width), Convert.ToInt32(-0.5 * enemy(i).height))
                    e.Graphics.RotateTransform(-enemy(i).angle * 180 / Math.PI)
                    e.Graphics.TranslateTransform(-enemy(i).x - 0.5 * enemy(i).width, -enemy(i).y - 0.5 * enemy(i).height)
                ElseIf enemy(i).hp = 2 And enemy(i).alive = 1 And enemy(i).type = 0 Then
                    e.Graphics.TranslateTransform(enemy(i).x + 0.5 * enemy(i).width, enemy(i).y + 0.5 * enemy(i).height)
                    e.Graphics.RotateTransform(enemy(i).angle * 180 / Math.PI)
                    e.Graphics.DrawImage(My.Resources.lightdamagedenemy, Convert.ToInt32(-0.5 * enemy(i).width), Convert.ToInt32(-0.5 * enemy(i).height))
                    e.Graphics.RotateTransform(-enemy(i).angle * 180 / Math.PI)
                    e.Graphics.TranslateTransform(-enemy(i).x - 0.5 * enemy(i).width, -enemy(i).y - 0.5 * enemy(i).height)
                ElseIf enemy(i).hp = 3 And enemy(i).alive = 1 And enemy(i).type = 0 Then
                    e.Graphics.TranslateTransform(enemy(i).x + 0.5 * enemy(i).width, enemy(i).y + 0.5 * enemy(i).height)
                    e.Graphics.RotateTransform(enemy(i).angle * 180 / Math.PI)
                    e.Graphics.DrawImage(My.Resources.enemy, Convert.ToInt32(-0.5 * enemy(i).width), Convert.ToInt32(-0.5 * enemy(i).height))
                    e.Graphics.RotateTransform(-enemy(i).angle * 180 / Math.PI)
                    e.Graphics.TranslateTransform(-enemy(i).x - 0.5 * enemy(i).width, -enemy(i).y - 0.5 * enemy(i).height)
                ElseIf enemy(i).alive = 0 And enemy(i).type = 1 Then
                    e.Graphics.TranslateTransform(enemy(i).x + 0.5 * enemy(i).width, enemy(i).y + 0.5 * enemy(i).height)
                    e.Graphics.RotateTransform(enemy(i).angle * 180 / Math.PI)
                    e.Graphics.DrawImage(My.Resources.stupiddeadenemy, Convert.ToInt32(-0.5 * enemy(i).width), Convert.ToInt32(-0.5 * enemy(i).height))
                    e.Graphics.RotateTransform(-enemy(i).angle * 180 / Math.PI)
                    e.Graphics.TranslateTransform(-enemy(i).x - 0.5 * enemy(i).width, -enemy(i).y - 0.5 * enemy(i).height)
                ElseIf enemy(i).hp = 1 And enemy(i).alive = 1 And enemy(i).type = 1 Then
                    e.Graphics.TranslateTransform(enemy(i).x + 0.5 * enemy(i).width, enemy(i).y + 0.5 * enemy(i).height)
                    e.Graphics.RotateTransform(enemy(i).angle * 180 / Math.PI)
                    e.Graphics.DrawImage(My.Resources.stupidheavydamagedenemy, Convert.ToInt32(-0.5 * enemy(i).width), Convert.ToInt32(-0.5 * enemy(i).height))
                    e.Graphics.RotateTransform(-enemy(i).angle * 180 / Math.PI)
                    e.Graphics.TranslateTransform(-enemy(i).x - 0.5 * enemy(i).width, -enemy(i).y - 0.5 * enemy(i).height)
                ElseIf enemy(i).hp = 2 And enemy(i).alive = 1 And enemy(i).type = 1 Then
                    e.Graphics.TranslateTransform(enemy(i).x + 0.5 * enemy(i).width, enemy(i).y + 0.5 * enemy(i).height)
                    e.Graphics.RotateTransform(enemy(i).angle * 180 / Math.PI)
                    e.Graphics.DrawImage(My.Resources.stupidlightdamagedenemy, Convert.ToInt32(-0.5 * enemy(i).width), Convert.ToInt32(-0.5 * enemy(i).height))
                    e.Graphics.RotateTransform(-enemy(i).angle * 180 / Math.PI)
                    e.Graphics.TranslateTransform(-enemy(i).x - 0.5 * enemy(i).width, -enemy(i).y - 0.5 * enemy(i).height)
                ElseIf enemy(i).hp = 3 And enemy(i).alive = 1 And enemy(i).type = 1 Then
                    e.Graphics.TranslateTransform(enemy(i).x + 0.5 * enemy(i).width, enemy(i).y + 0.5 * enemy(i).height)
                    e.Graphics.RotateTransform(enemy(i).angle * 180 / Math.PI)
                    e.Graphics.DrawImage(My.Resources.stupidenemy, Convert.ToInt32(-0.5 * enemy(i).width), Convert.ToInt32(-0.5 * enemy(i).height))
                    e.Graphics.RotateTransform(-enemy(i).angle * 180 / Math.PI)
                    e.Graphics.TranslateTransform(-enemy(i).x - 0.5 * enemy(i).width, -enemy(i).y - 0.5 * enemy(i).height)

                End If
            End If
        Next
        For a = 1 To bulletsquantity
            If bullet(a).active = 1 Then
                e.Graphics.DrawImage(My.Resources.bullet, Convert.ToSingle(bullet(a).x - bullet(a).width / 2), Convert.ToSingle(bullet(a).y - bullet(a).height / 2))
            End If
        Next
        e.Graphics.TranslateTransform(hero.x + 0.5 * hero.width, hero.y + 0.5 * hero.height)
        e.Graphics.RotateTransform(hero.angle * 180 / Math.PI)
        e.Graphics.DrawImage(My.Resources.hero, Convert.ToInt32(-0.5 * hero.width), Convert.ToInt32(-0.5 * hero.height))
        e.Graphics.RotateTransform(-hero.angle * 180 / Math.PI)
        e.Graphics.TranslateTransform(-hero.x + 0.5 * hero.width, -hero.y + 0.5 * hero.height)

    End Sub
    Private Sub Form1_KeyDown(ByVal sender As System.Object, ByVal e As System.Windows.Forms.KeyEventArgs) Handles MyBase.KeyDown
        Select Case e.KeyCode
            Case Keys.Space
                paused *= -1
            Case Keys.Enter
                main()
            Case Keys.Escape
                gameover()
            Case Keys.D
                rightbutton = 1
                hero.orientation = 4
            Case Keys.A
                leftbutton = 1
                hero.orientation = 3
            Case Keys.S
                downbutton = 1
                hero.orientation = 2
            Case Keys.W
                upbutton = 1
                hero.orientation = 1
        End Select
    End Sub
    Private Sub Form1_KeyUp(ByVal sender As System.Object, ByVal e As System.Windows.Forms.KeyEventArgs) Handles MyBase.KeyUp
        Select Case e.KeyCode
            Case Keys.D
                rightbutton = 0
            Case Keys.A
                leftbutton = 0
            Case Keys.S
                downbutton = 0
            Case Keys.W
                upbutton = 0
        End Select
    End Sub
    Private Sub PictureBox1_MouseMove(ByVal sender As System.Object, ByVal e As System.Windows.Forms.MouseEventArgs) Handles PictureBox1.MouseMove
        mousey = e.Y
        mousex = e.X
    End Sub
    Private Sub PictureBox1_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Forms.MouseEventArgs) Handles PictureBox1.MouseDown
        nowshooting = 1
    End Sub
    Private Sub PictureBox1_MouseUp(ByVal sender As System.Object, ByVal e As System.Windows.Forms.MouseEventArgs) Handles PictureBox1.MouseUp
        nowshooting = 0
        timewhenshooting = 0
    End Sub
End Class