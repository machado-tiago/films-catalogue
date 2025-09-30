package controller;

import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.Response;
import model.Movie;
import service.MovieService;

@Path("/movie")
@Produces("application/json")
@Consumes("application/json")
public class MovieController {

    @Inject
    MovieService movieService;

    @GET
    public Response buscarTodos() {
        return Response.ok(movieService.buscarTodos()).build();
    }

    @GET
    @Path("/{id}}")
    public Response buscarPorId(@PathParam("id") Long id) {
        return movieService.buscarPorId(id)
                .map(movie -> Response.ok(movie).build())
                .orElse(Response.status(Response.Status.NOT_FOUND).build()) ;
    }

    @POST
    @Transactional
    public Response criarRegistro(@Valid @NotNull  Movie movie) {
        return Response.status(Response.Status.CREATED).entity(movieService.criarRegistro(movie)).build();
    }

    @Transactional
    @PUT
    @Path("/{id}")
    public Response atualizar(@PathParam("id") Long id, @Valid @NotNull Movie movie) {
        return Response.ok(movieService.atualizar(id, movie)).build();
    }

    @Transactional
    @DELETE
    @Path("/{id}")
    public Response deletar(@PathParam("id") Long id) {
        if (movieService.deletar(id)) {
            return Response.noContent().build();
        } else {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
    }
}
