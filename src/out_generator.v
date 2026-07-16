module out_generator (
    input wire [1:0] red, green, blue,
    input wire hsync, vsync, video_active,
    output reg [7:0] uo_out
);
    always @(*) begin
        uo_out[7] = hsync;
        uo_out[3] = vsync;
        if (~video_active) begin
            uo_out[6:4] = 0;
            uo_out[2:0] = 0;
        end
        else begin
            uo_out[4] = red[0];
            uo_out[5] = green[0];
            uo_out[6] = blue[0];
            uo_out[0] = red[1];
            uo_out[1] = green[1];
            uo_out[2] = blue[1];
        end
    end

endmodule
