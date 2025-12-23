<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/create-session', function (){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});

Route::put('/update-stock', function(){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});
