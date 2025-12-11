<?php

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Route;

Route::get('/logout', function (){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});

Route::get('/login', function(){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});

Route::post('/add-item', function(){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});

Route::delete('/delete-item', function(){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});

Route::put('/update-item', function(){
    return response()->json([
        'message' => 'not implemented'
    ], 501);
});
