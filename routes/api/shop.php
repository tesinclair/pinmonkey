<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/', function(){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});
