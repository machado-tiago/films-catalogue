package repository;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import model.Avaliacao;

@ApplicationScoped
public class AvaliacaoRepository implements PanacheRepository<Avaliacao> {
}
