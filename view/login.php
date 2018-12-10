<!doctype html>
<html>
<head>
    <title>Register</title>
    
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
</head>
<body>
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #000000">
        <div class="container">
            <a class="navbar-brand" href="login.php">
                <!-- <img src="img/restaurant.png" width="30" height="30" class="d-inline-block align-top" alt=""> -->
                <b>Cloud Comp</b>
            </a>
            <ul class="nav navbar-nav navbar-right" style="padding-right: 40px">
              <li class="li_nav">
                <a href="login.php">Login</a>
              </li>
              <li class="li_nav">
                <a href="register.php">Register</a>
              </li>
            </ul>
        </div>
            
    </nav>
    <main role="main" class="container" style="margin-top: 40px">
        <div class="col-md-12">
            <div class="modal-dialog" style="margin-bottom:0">
                <div class="modal-content">
                            <div class="panel-heading">
                                <h3 class="panel-title">Sign In</h3>
                            </div>
                            <div class="panel-body">
                                <form role="form">
                                    <fieldset>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="E-mail" name="email" type="email" autofocus="">
                                        </div>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Password" name="password" type="password" value="">
                                        </div>
                                        <div class="checkbox">
                                            <label>
                                                <input name="remember" type="checkbox" value="Remember Me">Remember Me
                                            </label>
                                        </div>
                                        <!-- Change this to a button or input when using this as a form -->
                                        <a href="javascript:;" class="btn btn-sm btn-success">Login</a>
                                    </fieldset>
                                </form>
                            </div>
                        </div>
            </div>
        </div>
        
    </main>
</body>
</html>