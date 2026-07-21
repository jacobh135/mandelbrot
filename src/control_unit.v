module control_unit (
    input wire cranker_done,
    input wire signed [10:0] x_t, y_t,
    output wire time_enable, cranker_enable, count_advance, count_capture
);
    assign time_enable = cranker_done;
    assign cranker_enable = (((x_t[4:0] == 5'b00000) || (x_t == -11'sd1)) && (x_t < 640) && (y_t < 480));
    assign count_advance = ((x_t[4:0] == 5'b11111) && (x_t < 640) && (y_t < 480));
    assign count_capture = cranker_done;

endmodule