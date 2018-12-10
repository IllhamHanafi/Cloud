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
    <main role="main" class="container" style="margin-top: 40px">
        <div class="panel panel-default">
        <div class="panel-heading" style="background-color: #013880;color: white;">
                <b>Mahasiswa</b>
        </div>
        <div class="panel-body">
            <div class="table table-responsive">
                <table class="table table-bordered table-striped">
                    <thead>
                        <tr>
                        <th>#</th>
                        <th>NRP</th>
                        <th>Nama Mahasiswa</th>
                        <th>Angkatan</th>
                        <th>action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td> 1</td>
                            <td> Kamu</td>
                            <td> Tupai Hitam</td>
                            <td> 2015</td>
                            <td> <a href="#" class="btn btn-danger">Delete</a>
                                <a href="#" class=" btn btn-primary">Edit</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    </main>
</body>
</html>