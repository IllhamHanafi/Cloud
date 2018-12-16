<!doctype html>
<html>
<head>
    <title>Upload</title>
    
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
</head>
<body>
    <!--  -->
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #000000">
        <div class="container">
            <a class="navbar-brand" href="login.php">
                <!-- <img src="img/restaurant.png" width="30" height="30" class="d-inline-block align-top" alt=""> -->
                <b>Cloud Comp</b>
            </a>
            <ul class="nav navbar-nav navbar-right" style="padding-right: 40px">
              <li class="li_nav">
                <a href="home.php">Home</a>
              </li>
              <li class="li_nav">
                <a href="upload.php">Upload</a>
              </li>
              <li class="li_nav">
                <a href="login.php">Logout</a>
              </li>
            </ul>
        </div>
    </nav>
    
    <!--  -->
    <main role="main" class="container" style="margin-top: 40px">
        <form class="form-horizontal">

            <div class="form-group">
                <label class="control-label col-sm-2" for="">File (.jpg, .png)</label>
                <div class="col-sm-10">
                    <input type="file" class="form-control" name="file">
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-2" for="">Anda:</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="" placeholder="Kamu">
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-2" for="">Tupai:</label>
                <div class="col-sm-10"> 
                    <input type="password" class="form-control" id="" placeholder="Tupai Jantan">
                </div>
            </div>
            <div class="form-group"> 
                <div class="col-sm-offset-2 col-sm-10">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </div>
            </div>
        </form>
    </main>
</body>
</html>